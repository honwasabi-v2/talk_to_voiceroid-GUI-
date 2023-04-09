# talk_to_voiceroid
●プログラム説明  
AIとVOICEROIDで会話するpythonプログラム（GUI版）

●内容  
openAI.py:	openAIのAPIを利用して文字列から返答を用意し，返答を成形する  
A3RT.py:		RECRUITのA3RT APIを利用して文字列から返答を用意し，返答を成形する．  
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
 
	


