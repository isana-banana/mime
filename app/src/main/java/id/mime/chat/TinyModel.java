package id.mime.chat;

import android.content.Context;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

/** CPU inference engine matching the 298,656-parameter Python model. */
final class TinyModel {
    private static final int V=258, D=96, BLOCK=128, HEADS=4, HD=24, FF=256;
    private final float[] tok, pos, fnw, fnb;
    private final Layer[] layers = new Layer[3];
    private final Random random = new Random();

    private static final class Layer {
        float[] n1w,n1b,qw,qb,pw,pb,n2w,n2b,w1,b1,w2,b2;
    }

    TinyModel(Context context) throws IOException {
        DataInputStream in = new DataInputStream(context.getAssets().open("mime300k.bin"));
        byte[] magic = new byte[8]; in.readFully(magic);
        if (!Arrays.equals(magic, "MIME300K".getBytes(StandardCharsets.US_ASCII)))
            throw new IOException("Invalid 300K model asset");
        int count=in.readInt();
        if(count!=40) throw new IOException("Unexpected tensor count: "+count);
        tok=read(in, V*D); pos=read(in, BLOCK*D);
        for(int i=0;i<3;i++) {
            Layer l=new Layer();
            l.n1w=read(in,D); l.n1b=read(in,D);
            l.qw=read(in,3*D*D); l.qb=read(in,3*D);
            l.pw=read(in,D*D); l.pb=read(in,D);
            l.n2w=read(in,D); l.n2b=read(in,D);
            l.w1=read(in,FF*D); l.b1=read(in,FF);
            l.w2=read(in,D*FF); l.b2=read(in,D);
            layers[i]=l;
        }
        fnw=read(in,D); fnb=read(in,D);
        if(in.read()!=-1) throw new IOException("Unexpected trailing model data");
        in.close();
    }

    private static float[] read(DataInputStream in,int expected)throws IOException {
        int n=in.readInt();
        if(n!=expected) throw new IOException("Tensor size mismatch: expected "+expected+", got "+n);
        float[] a=new float[n]; for(int i=0;i<n;i++) a[i]=in.readFloat(); return a;
    }

    private static float[] norm(float[] x,int t,float[] w,float[] b) {
        float mean=0; for(int j=0;j<D;j++) mean+=x[t*D+j]; mean/=D;
        float var=0; for(int j=0;j<D;j++){float z=x[t*D+j]-mean;var+=z*z;} var/=D;
        float inv=(float)(1.0/Math.sqrt(var+1e-5)); float[] y=new float[D];
        for(int j=0;j<D;j++) y[j]=(x[t*D+j]-mean)*inv*w[j]+b[j];
        return y;
    }

    private static float[] linear(float[] x,int rows,int in,int out,float[] w,float[] b) {
        float[] y=new float[rows*out];
        for(int r=0;r<rows;r++) for(int o=0;o<out;o++) {
            float s=b[o]; int wi=o*in, xi=r*in;
            for(int k=0;k<in;k++) s+=x[xi+k]*w[wi+k];
            y[r*out+o]=s;
        }
        return y;
    }

    private static float gelu(float x) {
        double c=0.7978845608*(x+0.044715*x*x*x);
        return (float)(0.5*x*(1.0+Math.tanh(c)));
    }

    private float[] forward(int[] ids) {
        int n=ids.length; float[] x=new float[n*D];
        for(int t=0;t<n;t++) for(int j=0;j<D;j++) x[t*D+j]=tok[ids[t]*D+j]+pos[t*D+j];
        for(Layer l:layers) {
            float[] a=new float[n*D];
            for(int t=0;t<n;t++) System.arraycopy(norm(x,t,l.n1w,l.n1b),0,a,t*D,D);
            float[] qkv=linear(a,n,D,3*D,l.qw,l.qb), att=new float[n*D];
            for(int t=0;t<n;t++) for(int h=0;h<HEADS;h++) {
                float[] scores=new float[t+1]; float max=-Float.MAX_VALUE;
                for(int s=0;s<=t;s++) {
                    float dot=0;
                    for(int k=0;k<HD;k++) dot+=qkv[t*3*D+h*HD+k]*qkv[s*3*D+D+h*HD+k];
                    scores[s]=dot*(1.0f/(float)Math.sqrt(HD)); if(scores[s]>max) max=scores[s];
                }
                float sum=0;
                for(int s=0;s<=t;s++){scores[s]=(float)Math.exp(scores[s]-max);sum+=scores[s];}
                for(int s=0;s<=t;s++) {
                    float p=scores[s]/sum;
                    for(int k=0;k<HD;k++) att[t*D+h*HD+k]+=p*qkv[s*3*D+2*D+h*HD+k];
                }
            }
            float[] projected=linear(att,n,D,D,l.pw,l.pb);
            for(int i=0;i<x.length;i++) x[i]+=projected[i];
            float[] z=new float[n*D];
            for(int t=0;t<n;t++) System.arraycopy(norm(x,t,l.n2w,l.n2b),0,z,t*D,D);
            float[] hidden=linear(z,n,D,FF,l.w1,l.b1);
            for(int i=0;i<hidden.length;i++) hidden[i]=gelu(hidden[i]);
            float[] out=linear(hidden,n,FF,D,l.w2,l.b2);
            for(int i=0;i<x.length;i++) x[i]+=out[i];
        }
        float[] last=norm(x,n-1,fnw,fnb), logits=new float[V];
        for(int v=0;v<V;v++) {
            float s=0; for(int j=0;j<D;j++) s+=last[j]*tok[v*D+j]; logits[v]=s;
        }
        return logits;
    }

    private static String decodeUtf8Safely(byte[] bytes) {
        ByteBuffer input=ByteBuffer.wrap(bytes); CharBuffer chars=CharBuffer.allocate(bytes.length+1);
        StringBuilder decoded=new StringBuilder();
        java.nio.charset.CharsetDecoder decoder=StandardCharsets.UTF_8.newDecoder()
            .onMalformedInput(CodingErrorAction.REPORT).onUnmappableCharacter(CodingErrorAction.REPORT);
        while(input.hasRemaining()) {
            java.nio.charset.CoderResult result=decoder.decode(input,chars,true);
            chars.flip(); decoded.append(chars); chars.clear();
            if(result.isError()) input.position(Math.min(input.limit(),input.position()+result.length()));
            else break;
        }
        StringBuilder clean=new StringBuilder();
        for(int i=0;i<decoded.length();) {
            int cp=decoded.codePointAt(i); i+=Character.charCount(cp);
            if(cp==0xfffd) continue;
            if(Character.isISOControl(cp)&&cp!='\n'&&cp!='\t') continue;
            clean.appendCodePoint(cp);
        }
        return clean.toString().trim();
    }

    String reply(String prompt,int maxNew,float temperature,int topK) {
        byte[] bytes=prompt.getBytes(StandardCharsets.UTF_8);
        int take=Math.min(bytes.length,BLOCK-1); int[] ids=new int[take+1]; ids[0]=256;
        for(int i=0;i<take;i++) ids[i+1]=bytes[bytes.length-take+i]&255;
        ByteArrayOutputStream output=new ByteArrayOutputStream();
        for(int step=0;step<maxNew;step++) {
            int start=Math.max(0,ids.length-BLOCK);
            int[] ctx=Arrays.copyOfRange(ids,start,ids.length);
            float[] logits=forward(ctx);
            for(int i=0;i<logits.length;i++) logits[i]/=Math.max(temperature,0.05f);
            logits[256]=Float.NEGATIVE_INFINITY;
            Integer[] order=new Integer[V-1]; int oi=0;
            for(int i=0;i<V;i++) if(i!=256) order[oi++]=i;
            Arrays.sort(order,(a,b)->Float.compare(logits[b],logits[a]));
            boolean[] allowed=new boolean[V];
            for(int i=0;i<Math.min(Math.max(topK,1),order.length);i++) allowed[order[i]]=true;
            float max=logits[order[0]],sum=0;
            for(int i=0;i<V;i++) {
                if(allowed[i]) {logits[i]=(float)Math.exp(logits[i]-max);sum+=logits[i];}
                else logits[i]=0;
            }
            double r=random.nextDouble()*sum; int next=order[0];
            for(int i=0;i<V;i++) if(allowed[i]) {r-=logits[i];if(r<=0){next=i;break;}}
            if(next==257) break;
            if(next<0||next>255) continue;
            output.write(next);
            ids=Arrays.copyOf(ids,ids.length+1); ids[ids.length-1]=next;
        }
        return decodeUtf8Safely(output.toByteArray());
    }
}
