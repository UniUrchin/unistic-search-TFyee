# unisticsearch-ft-yee

占いサイトの情報をスクレイピングで集めまくって統合的に運勢の分析を行うPythonスクリプト。

YeeLightと連動させることにより、占い中にいい感じのムードを演出してくれるようになる。

## Requirement

- Python 10.3.6
- YeeLight 

  - 型番: YLDP13DLでの動作は確認済み
  - 仮に物理デバイスが無くても、Yeelightの処理部分をコメントアウトすればCLI占いとして動く

## How to Execute

- YeeLightの電源を入れて、ローカルネットワークから接続できる状態にする

  - アプリからLAN経由で操作できるような状態になっていればOK!!

- unisticsearch-ft-yeeを実行する

```
$ python3 usft_yee.py
```

## Usage

### 占い情報を手動で入力する場合

usft_yee.pyを実行すると、YeeLightのIPアドレスを探索するフェーズに入るので少し待つ。

```
==========================
 - Unisticsearch-FT-Yee -
==========================
Discover Yeelight on your local network...
Success: Your Yeelight's IP address is "***.***.***.***"
```

分析したい誕生日を"YYYY-MM-DD"の形式で入力する。

```
Enter the information required for fortune-telling
Type your birthday (Ex: 2012-09-13)
>>> 1111-11-11
```

分析したい誕生日を"A、B、O、AB"の中から入力する。

```
Type your blood type (Ex: A | B | O | AB)
>>> A
```

サイトのスクレイピングが始まるので、YeeLightの光の変化を楽しみながら気長に待っておく。

```
Start today's fortune-telling analysis...

VOGUE HOROSCOPE: https://www.vogue.co.jp/horoscope（蠍座の運勢）
Success: The average score for VOGUE HOROSCOPE is 40 points

Nippon TV Sukkirisu https://ntv.co.jp/sukkiri/sukkirisu（11月生まれの運勢）
Success: The average score for Nippon TV Sukkirisu is 68 points

URANAI Square: https://uranai.d-square.co.jp（A型の運勢）
Success: The average score for URANAI Square is 10 points

LINE Fortune: https://fortune.line.me（蠍座の運勢）
Success: The average score for LINE Fortune is 35 points

ESTART Uranai https://start.jword.jp/uranai（11月生まれの運勢）
Success: The average score for ESTART Uranai is 77 points
```

統合的な運勢と今日のラッキーリスト(TTL)が表示される。

```
Result: Your today's fortune is "小吉"(46points)!!
------------------------------
 - Today's Lucky List (TLL) -
------------------------------
  - ピローミスト
  - 紫
  - 山吹色
  - 三つ編み・編み込みスタイル
  - 包装紙
  - 紫
  - ヘアブラシ <- Recommended!!
  - 黒
  - 数字の1
------------------------------
Press Enter key to exit the program...
```

### 占い情報をファイルから読み取る場合

占い情報を以下のようなJSON形式(ftprofile)として保存することで、`-f`引数にファイル名を指定するとそこから占い情報を読み込んで実行してくれる。

```
{
  "birthday": "1111-11-11",
  "blood_type": "A"
}
```

誕生日と血液型の入力が不要になるため、占いの自動実行などに使えるかも。

```
$ python3 usft_yee.py -f ./ftprofile/sample.json

==========================
 - Unisticsearch-FT-Yee -
==========================
Discover Yeelight on your local network...
Success: Your Yeelight's IP address is "***.***.***.***"

Loading required information for fortune-telling
Start today's fortune-telling analysis...
```

### もう少し詳しく占いの内容が知りたい!!

引数として`-v`を指定することで、平均スコアの表示に加えてアドバイスや具体的なスコアリングなどの詳細情報を表示してくれるようになる。

```
$ python3 usft_yee.py -v

==========================
 - Unisticsearch-FT-Yee -
==========================

(中略)

VOGUE HOROSCOPE: https://www.vogue.co.jp/horoscope（乙女座の運勢）
  Love luck:
    star: ★ ☆ ☆ ☆ ☆  (20points)
    advice: 波乱運
            年長者のアドバイスから恋のヒントが得られそう
            ただ、行動に移すのはもう少し先です
            今日は大人しく過ごした方が良いでしょう
  Interparsonal luck:
    star: ★ ★ ☆ ☆ ☆  (40points)
    advice: 自重運
            普段の何気ない会話から、相手の真意を見出してみよう
            意外な一面を発見できるかも
            コミュニケーションを疎かにしないことが大切
  Work and Study luck:
    star: ★ ★ ★ ☆ ☆  (60points)
    advice: 吉凶混合運
            誤字・脱字などの小さなミスが頻発します
            逆にそうしたケアレスミスを意識する習慣をつけると今後のあなたの糧に
  Money luck:
    star: ★ ★ ☆ ☆ ☆  (40points)
    advice: 自重運
            収入アップを望むあまり、詐欺などに引っかかってしまうかも
            おいしすぎる話は、疑ってかかるように注意しましょう
  Health and Beauty luck:
    star: ★ ☆ ☆ ☆ ☆  (20points)
    advice: 波乱運
            気分も体調もどんよりして、ボンヤリしがち……
            無理をすると悪化すると暗示があるので、今日はゆっくり休養しましょう
  Lucky item:
    name: ルーペ
Success: The average score for VOGUE HOROSCOPE is 20 points

(中略)
```

## Features

### スクレイピング先のサイト一覧

unisticsearch-ft-yeeでは、以下のサイトをスクレイピングして統合占い分析に使用します。

- **VOGUE HOROSCOPE**
  - https://www.vogue.co.jp/horoscope
  - 恋愛運、対人運、仕事・勉強運、マネー運、ヘルス&ビューティー運を5段階評価し、それぞれの平均スコアを取り込む
  - ラッキーアイテムをラッキーリストに追加する

- **スッキりす!!**
  - https://ntv.co.jp/sukkiri/sukkirisu
  - "超スッキりす"、"スッキりす"、"まぁまぁスッキりす"、"ガッカりす"の区分に応じてスコアを割り振る
  - ラッキーカラーをラッキーリストに追加する

- **占いスクエア**
  - https://uranai.d-square.co.jp
  - 良い運勢を持つ血液型の順位によってスコアを割り振る
  - ラッキーカラーとラッキーワードをラッキーリストに追加する

- **LINE占い**
  - https://fortune.line.me
  - 総合運、恋愛運、金運、仕事運を10段階評価し、それぞれの平均スコアを取り込む
  - ラッキーアイテムとラッキーカラーをラッキーリストに追加する

- **ESTART 誕生月占い**
  - https://start.jword.jp/uranai
  - 総合運、恋愛運、金銭運、仕事運を3段階評価し、それぞれの平均スコアを取り込む
  - ラッキーアイテム、ラッキーカラー、ラッキーナンバーをラッキーリストに追加する

### 統合的な運勢の結果とYeeLightの光り方

最終的に運勢は100点満点で評価され、点数によってYeeLightの光り方が変わります。

- **大吉**: 80点〜100点の時、YeeLightがマゼンタ色になって光る

- **中吉**: 60点〜79点の時、YeeLightが黄色になって光る

- **小吉**: 40点〜59点の時、YeeLightが黄緑色になって光る

- **末吉**: 20点〜39点の時、YeeLightが水色になって光る

- **凶**: 0点〜19点の時、YeeLightが紫色になり光る

また、今日のラッキーリスト(TTL)のオススメは一番高得点を叩き出したスクレイピングサイトから抽出したラッキーリストからランダムに選ばれる仕様になっている。