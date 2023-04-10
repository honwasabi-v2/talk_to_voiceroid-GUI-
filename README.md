# talk_to_voiceroid(GUI)  
●プログラム説明  
AIとVOICEROIDで会話するpythonプログラム（GUI版） 

●内容  
openAI.py:	openAIのAPIを利用して文字列から返答を用意し，返答を成形する  
A3RT.py:		RECRUITのA3RT APIを利用して文字列から返答を用意し，返答を成形する 
speech_to_text.py:	音声をpyaudioを用いて処理する．音声をoutput.wavに保存し，wavファイルからテキストにする．   
text_to_speech.py:	pyvcroid2を用いて文字列をVOICEROIDでvoiceroid.wavに出力＆発声  
main.py:	GUI他メイン処理  　　
config.json:  APIのキー等の設定ファイル  
requirements.txt:　必要なライブラリ一覧  
dummy.png:  口パク表示のダミーファイル  

●実行に必要なもの  
・RECRUITのA3RT(https://a3rt.recruit.co.jp/ )かopenAI(https://openai.com/blog/openai-api )のAPIKey  
・pyvcroid2 (https://github.com/Nkyoku/pyvcroid2 )   
・VOICEROID2本体  
・python    
pythonとVOICEROIDは32bit版か64bit版で統一しないといけないようです  


●前準備    
1.config.jsonを入力  
&ensp; 1.1利用したいAPIのキーを取得し，"key"のうち利用するAPIの値"--key--"を書き換える（利用するAPIだけでok） 　　
&ensp; 1.2利用したいAPIを"api"の値を書き換える（"A3RT"もしくは"openAI"）  
&ensp; 1.3画像を入れたい場合はfigureの"figure/dummy.png"に画像のパスを入力する（open:口開け，half:半開き，close:口閉じ）  
2.main.pyを実行する（必要なライブラリはrequirement.txtに記載している.......多分）    

●利用方法   
    〇下のテキストエリアに文字を入力して送信ボタンを押すと上のテキストエリアに返事が返ってきてVOICEROID2が読み上げてくれます   
    〇録音開始ボタンを押すと声を認識し，上のテキストエリアに返事が返ってきてVOICEROID2が読み上げてくれます    
    〇録音終了ボタンを押すと現在の録音が終わり次第，音声認識を終了します  
    〇右のスライダーで読み上げるVOICEROID2のパラメータを変更できます（キャラクター，音量，スピード等）  


●今後UIは変更するかもしれません  

 
	


