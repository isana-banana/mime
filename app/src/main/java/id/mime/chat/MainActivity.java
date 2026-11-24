package id.mime.chat;

import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends Activity {
    private LinearLayout messages;
    private EditText input;
    private Button send;
    private TextView status;
    private TinyModel model;
    private final ExecutorService worker=Executors.newSingleThreadExecutor();

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(246,247,249));
        getWindow().setNavigationBarColor(Color.rgb(246,247,249));
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR|View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
        LinearLayout root=new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.rgb(246,247,249));
        TextView title=new TextView(this); title.setText("MIME Chat 300K");
        title.setTextColor(Color.rgb(25,35,50)); title.setTextSize(22);
        title.setTypeface(null,Typeface.BOLD); title.setPadding(20,18,20,2); root.addView(title);
        status=new TextView(this); status.setText("Memuat model 300K lokal…");
        status.setTextColor(Color.GRAY); status.setTextSize(12);
        status.setPadding(20,0,20,12); root.addView(status);
        ScrollView scroll=new ScrollView(this);
        messages=new LinearLayout(this); messages.setOrientation(LinearLayout.VERTICAL);
        messages.setPadding(14,12,14,12); scroll.addView(messages);
        root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
        TextView note=new TextView(this);
        note.setText("298.656 parameter · offline · model eksperimen, jawaban mungkin belum koheren");
        note.setTextColor(Color.GRAY); note.setTextSize(11); note.setPadding(16,6,16,6); root.addView(note);
        LinearLayout bar=new LinearLayout(this); bar.setPadding(12,8,12,12);
        bar.setGravity(Gravity.CENTER_VERTICAL);
        input=new EditText(this); input.setSingleLine(false); input.setMaxLines(3);
        input.setHint("Tulis pesan…"); input.setTextSize(15);
        bar.addView(input,new LinearLayout.LayoutParams(0,-2,1));
        send=new Button(this); send.setText("Kirim"); bar.addView(send); root.addView(bar);
        setContentView(root);
        addMessage("MIME","Halo! Aku MIME-ID 300K. Coba ajak aku berbicara. Ini masih model eksperimen kecil.",false);
        send.setOnClickListener(v->submit(scroll)); send.setEnabled(false);
        worker.execute(()->{
            try {
                TinyModel loaded=new TinyModel(this);
                runOnUiThread(()->{model=loaded;status.setText("Model siap · offline");send.setEnabled(true);});
            } catch(Exception e) {
                runOnUiThread(()->status.setText("Gagal memuat model: "+e.getMessage()));
            }
        });
    }

    private void submit(ScrollView scroll) {
        String text=input.getText().toString().trim();
        if(text.isEmpty()||model==null)return;
        input.setText("");
        ((InputMethodManager)getSystemService(Context.INPUT_METHOD_SERVICE))
            .hideSoftInputFromWindow(input.getWindowToken(),0);
        addMessage("Kamu",text,true); send.setEnabled(false); status.setText("MIME sedang berpikir…");
        worker.execute(()->{
            String answer;
            try {
                answer=model.reply("Pengguna: "+text+"\nAsisten:",96,0.8f,40);
                if(answer.isEmpty())answer="(Model tidak menghasilkan teks.)";
            } catch(Exception e) {answer="Terjadi kesalahan saat inferensi: "+e.getMessage();}
            final String result=answer;
            runOnUiThread(()->{
                addMessage("MIME",result,false); send.setEnabled(true);
                status.setText("Model siap · offline"); scroll.post(()->scroll.fullScroll(View.FOCUS_DOWN));
            });
        });
    }

    private void addMessage(String who,String body,boolean user) {
        LinearLayout wrap=new LinearLayout(this); wrap.setOrientation(LinearLayout.VERTICAL);
        wrap.setGravity(user?Gravity.RIGHT:Gravity.LEFT);
        TextView label=new TextView(this); label.setText(who); label.setTextColor(Color.GRAY);
        label.setTextSize(11); label.setPadding(6,4,6,3); wrap.addView(label);
        TextView bubble=new TextView(this); bubble.setText(body);
        bubble.setTextColor(Color.rgb(30,38,48)); bubble.setTextSize(15);
        bubble.setPadding(14,10,14,10);
        GradientDrawable bg=new GradientDrawable();
        bg.setColor(user?Color.rgb(220,235,255):Color.WHITE); bg.setCornerRadius(18);
        bubble.setBackground(bg);
        LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(
            (int)(getResources().getDisplayMetrics().widthPixels*0.82),-2);
        bp.bottomMargin=10; wrap.addView(bubble,bp); messages.addView(wrap);
    }

    @Override protected void onDestroy() {super.onDestroy();worker.shutdown();}
}
