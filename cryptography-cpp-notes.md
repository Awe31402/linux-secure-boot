# 讀書筆記：Practical Cryptography

> 《*Practical Cryptography: Algorithms and Implementations Using C++*》
> （Saiful Azad、Al-Sakib Khan Pathan 編，CRC Press / Auerbach，2015）的讀書筆記。
> 規格見 [cryptography-cpp-notes-brief.md](./cryptography-cpp-notes-brief.md)。
>
> **這份筆記是主要閱讀物，書是查證來源。** 從零開始，不假設任何背景。
>
> **語言**：中文為主，專有名詞保留英文（書是英文的，查書時要對得上）。
>
> **📄 原文**：每節附書頁 ｜ PDF 頁 ｜ 可點連結。
> **書頁 + 22 = PDF 頁，全書固定**（14 章章名頁已逐章核對，換算表見 brief）。
>
> **💻 程式碼對照**：書上哪個函式在做哪一步，只引關鍵幾行，完整實作請翻書。
>
> **⚠️ 標記**：書上沒有的、已過時的、我自己補的、以及**書上前後不一致**的地方，
> 一律標出來。
>
> **範圍**：第 1～11 章。第 12～14 章是研究論文調性，列為非目標（見結尾一節）。

---

## ⚠️ 讀這本書之前必須先知道的一件事

**書上印出來的 C++ 程式碼，照抄不會過編譯。**

不是排版偶爾出錯，是**系統性的**。看書頁 13 印出來的樣子：

```cpp
charcaesar(char c, int k)//'c' holds the letter to be
if(isalpha(c) && c ! = toupper(c))
for(inti = 0; i< 26; i++) {
```

該有的空格被吃掉（`char caesar` → `charcaesar`、`int i` → `inti`），
不該有的空格被插進去（`!=` → `! =`、`==` → `= =`、`+=` → `+ =`），
直引號被排版成全形彎引號（`"` → `“ ”`、`'` → `‘ ’`）。

看起來是排版流程把原始碼的空白正規化了，而**出版前沒有人把它編譯回去驗證**。

> **這份筆記引用程式碼時照書原樣呈現**，不默默幫書修好 ——
> 否則你翻書對照時會以為是自己打錯。需要正確寫法時另外標一行。

---
---

# 第 1 章 資訊安全與密碼學基礎

**Basics of Security and Cryptography** ｜ 作者 Al-Sakib Khan Pathan
書頁 1–10 ｜ PDF 23–32 ｜ [開啟](./cryptography-cpp.pdf#page=23)

> 書上只編了兩個小節號（1.1、1.2），前面六頁是一整片沒有編號的定義清單。
> 這裡的分節是我加的 —— 順序沒動，只是把書沒編號的地方補上編號。

## §1.0 這章在解什麼問題

把後面十章會反覆用到的字先講清楚。

這章沒有演算法、沒有程式碼、沒有數學，就是一份名詞表加兩節討論。
**但它決定了你後面十章讀起來會不會一直卡住** —— 因為 cryptography 這個領域裡，
「加密」「編碼」「雜湊」「簽章」在日常中文裡都被含糊地叫做「加密」，
而在這本書裡它們是四件完全不同的事。

作者自己講了這章的定位：

> 📄 **原文**　書 p.1 ｜ PDF p.23 ｜ [開啟](./cryptography-cpp.pdf#page=23)
>
> [...] the intent of this first chapter is to set the basics for the rest of
> the content.

## §1.1 三個最基本的字：plaintext、ciphertext、cipher

**Plaintext（明文）**：你本來想傳的訊息。書說它的同義詞是 cleartext。

**Encryption（加密）**：把明文變成看不懂的東西的**過程**。

**Ciphertext（密文）**：加密之後的結果。

**Cipher（密碼演算法）**：**執行**加解密的那一套明確定義的步驟。
書特別註明它也被叫做 cryptoalgorithm。

### 為什麼要分「過程」和「演算法」兩個字

初學者最容易在這裡打結：encryption 和 cipher 聽起來是同一件事。

差別在於 —— **cipher 是一個名詞、一份規格、一個可以寫成程式的東西**；
encryption 是你**拿那份規格去跑**的動作。

打個比方：食譜是 cipher，照著食譜做菜是 encryption，做出來的菜是 ciphertext。

這個區分之所以重要，是因為**同一個 cipher 配不同的金鑰會產生不同的 ciphertext**——
下一節就會看到，安全性靠的是金鑰，不是食譜。

### 加密不是編碼

⚠️ **本段不是書上的內容。** 書沒有講這個區分，但它是初學者最常見的誤解，
而且會一路誤解到第 10 章。

- **Encoding（編碼）**：Base64、UTF-8、URL encoding。目的是**格式轉換**，
  任何人都能還原，**沒有金鑰**。
- **Encryption（加密）**：目的是**保密**，沒有金鑰就還原不了。

「我把密碼 Base64 之後存起來」不是加密，是把明文換一種寫法。

## §1.2 金鑰（cryptographic key）到底是什麼

書給的定義：

> 📄 **原文**　書 p.3 ｜ PDF p.25 ｜ [開啟](./cryptography-cpp.pdf#page=25)
>
> A key is a piece of information (or a parameter) that determines the
> functional output of a cryptographic algorithm or cipher.

翻成白話：**演算法是公開的、固定的；金鑰是秘密的、可換的。**
同一個演算法，換一把金鑰，輸出就完全不同。

這是整本書、也是整個現代密碼學的前提：

> **安全性必須完全來自「金鑰保密」，不能來自「演算法保密」。**

為什麼？因為演算法會外流 —— 被反組譯、被離職員工帶走、被論文發表。
金鑰外流你可以換一把；演算法外流你得換整個系統。
而且公開的演算法會被全世界的人攻擊，撐過來的才值得信任。

⚠️ **本段不是書上的內容。** 上面這條原則叫 **Kerckhoffs's principle**
（Kerckhoffs 原則，1883），**書上沒有提到這個名字**，但它是後面每一章的隱含前提。
第 2 章的四個古典密碼之所以全部「不安全」，判準就是它。

### ⚠️ 書上這句話會誤導人

> 📄 **原文**　書 p.3 ｜ PDF p.25
>
> Sometimes key means just some steps or rules to ­follow to twist the plaintext
> before transmitting it via a public medium.

**這句話跟上一段的定義互相矛盾。** 「要遵循的步驟或規則」那是 **cipher**，不是 key。
如果「步驟」本身就是秘密，那就是靠演算法保密 —— 正是 Kerckhoffs 原則否定的做法。

這句話大概是想描述古典密碼裡「金鑰和演算法糾纏在一起」的狀態
（例如 Playfair 的 5×5 矩陣，既像規則又像金鑰）。但寫成通則是錯的。
**記書上那個正式定義就好，這句忽略。**

## §1.3 兩種處理資料的方式：stream cipher 與 block cipher

書在這裡第一次把對稱式加密切成兩類，並各配一張圖。

### Stream cipher（串流密碼）—— 書上圖 1.1

**一次處理一個 bit（或一個 byte）。**

運作方式：金鑰 K 餵進一個 **pseudorandom byte generator（虛擬亂數產生器）**，
產生一長串看起來像亂數的位元流 k（叫 **key stream**），
再把 key stream 跟明文逐位元混合，產生密文。

解密端用**同一把金鑰**產生**同一串 key stream**，反向混合就還原了。

> 關鍵在於：兩端必須產生**完全相同**的 key stream。所以那個「亂數」產生器
> 必須是**可重現**的 —— 它叫 pseudorandom（虛擬亂數）而不是 random，就是這個原因。

### Block cipher（區塊密碼）—— 書上圖 1.2

**一次處理一整塊資料**，書舉的例子是連續 64 個 bit。

> 📄 **原文**　書 p.3 ｜ PDF p.25
>
> A block cipher is a method of encrypting text [...] applied to a block of data
> (for example, 64 ­contiguous bits) at once as a group rather than one bit at a time.

書上圖 1.2 裡有一條**虛線的 feedback（回饋）**，從密文區塊繞回下一個明文區塊。
書說這條線是**可選的**，但可以「強化」流程，並點名了一種模式：

> 📄 **原文**　書 p.3 ｜ PDF p.25
>
> A stronger mode is cipher feedback (CFB), which combines the plain block with
> the previous cipher block before encrypting it.

**這條虛線就是後面第 4 章 mode of operation（操作模式）的伏筆。**
現在只要記住一件事：**區塊密碼本身只會加密「一塊」，
怎麼把一長串資料切成很多塊、塊跟塊之間怎麼串，是另一個獨立的設計問題。**

### ⚠️ 書上這句話是錯的

> 📄 **原文**　書 p.3 ｜ PDF p.25
>
> [Stream cipher] This method is not much used in modern cryptography.

**2015 年寫這句就已經站不住，2026 年更是明確錯誤。**

串流密碼今天用得非常多 —— **ChaCha20**（配 Poly1305）是 TLS 1.3 的正式加密套件之一，
在沒有 AES 硬體指令的行動裝置與嵌入式平台上是主力選擇。

作者想講的大概是 **RC4** 的退場（RC4 曾經無所不在，2015 年前後被禁用）。
**但「RC4 死了」不等於「串流密碼死了」。**

> 這是本章唯一一句我判定為錯誤的技術陳述。記下來，不要背它。

## §1.4 cryptology、cryptography、cryptanalysis 三個字的關係

書把這三個字排在一起講，順序是：

- **Cryptology（密碼學，廣義）**：**傘狀名詞**，底下包含另外兩個。
  書強調它是數學（尤其數論）加上公式與演算法的那個領域。
- **Cryptography（密碼編碼學）**：**怎麼造**。書的定義是 "the science of information security"。
- **Cryptanalysis（密碼分析學）**：**怎麼破**。研究密碼、密文、密碼系統，
  找出弱點，讓人能在**不知道金鑰、甚至不知道演算法**的情況下還原明文。

> 📄 **原文**　書 p.4 ｜ PDF p.26 ｜ [開啟](./cryptography-cpp.pdf#page=26)
>
> cryptology is the umbrella term under which comes ­cryptography and cryptanalysis.

### 為什麼「怎麼破」和「怎麼造」是同一門學問

初學者常覺得 cryptanalysis 是「壞人做的事」。不是。

**一個密碼演算法的安全性，唯一的證據就是「很多聰明人認真攻擊過它，沒破」。**
沒有辦法證明一個演算法絕對安全（除了 one-time pad 那種特例），
只能累積「攻不破」的紀錄。所以攻擊研究就是安全性的來源。

這也解釋了第 2 章的體例：每個古典密碼都是
「**演算法 → 實作 → 為什麼會被破**」三段式 —— 第三段才是真正的知識。

> 書自己也承認 cryptography 和 cryptology 常被當同義詞混用。
> **實務上不用太計較，但考試或讀論文時要知道正式的包含關係。**

## §1.5 cryptosystem：把演算法湊成一個可用的系統

書給的定義很短：

> 📄 **原文**　書 p.4 ｜ PDF p.26
>
> A cryptosystem is a pair of algorithms that take a key and convert plaintext to
> ciphertext and back.

也就是：**一對演算法（加密 + 解密）＋ 一把金鑰**。

### ⚠️ 這個定義少了一塊

⚠️ **本段不是書上的內容。**

標準的定義是**三個**演算法，不是一對：

| 演算法 | 做什麼 | 書上有沒有 |
|---|---|---|
| **KeyGen（金鑰產生）** | 產生一把（或一對）金鑰 | ❌ **書的定義裡沒有** |
| **Encrypt（加密）** | 明文 + 金鑰 → 密文 | ✅ |
| **Decrypt（解密）** | 密文 + 金鑰 → 明文 | ✅ |

**漏掉 KeyGen 不是小事。** 現實世界裡絕大多數的密碼系統崩潰，
不是因為演算法被破，而是因為**金鑰產生得太爛**（可預測的亂數、寫死的種子、
從時間戳算出來的種子）。

**你會在第 3 章親眼看到這個坑** —— 那章的轉輪機實作用 `srand(5)`
產生轉子接線，固定種子代表**每次執行產生的機器完全一樣**，等於根本沒有金鑰。

而且**書全書沒有亂數產生（CSPRNG）的專章**（見本章結尾的缺口表）。

### 正確性條件

⚠️ **本段不是書上的內容。** 書沒有明寫，但這是隱含的要求：

對任何金鑰 K 和任何明文 M，必須滿足 **Decrypt(K, Encrypt(K, M)) = M**。

聽起來像廢話，但第 2、3 章的四份實作裡，**有兩份不滿足這個條件**
（Playfair 的 X 移除、轉輪機的計數器沒重置）。這條件不是自動成立的。

## §1.6 對稱式（symmetric）與公開金鑰（public-key）的第一次照面

### 對稱式加密 —— 書上圖 1.3

**加密和解密用同一把金鑰。** 圖 1.3 畫的是：Alice 用 shared secret key 加密，
Bob 用**同一把** shared secret key 解密，中間的密文對第三方是「??」。

書列了它的三個好處：

> 📄 **原文**　書 p.4 ｜ PDF p.26
>
> • It is relatively inexpensive to produce a strong key for these types of ciphers.
> • The keys tend to be much smaller in size for the level of protection they afford.
> • The algorithms are relatively inexpensive to process.

翻成白話：**金鑰好產、金鑰短、跑得快。** 三個都是效能上的優勢。

⚠️ **書沒有明講它的致命問題**：那把金鑰**要怎麼先送給對方**？
如果你有一條安全的管道可以送金鑰，那你為什麼不直接用那條管道送訊息？
這叫 **key distribution problem（金鑰分送問題）**，正是下一個模型存在的理由。
書把這個問題留到第 7 章才處理。

### 公開金鑰加密 —— 書上圖 1.4

**兩把金鑰，一把公開（public key）一把私藏（private key）**，
書強調兩者「different, but mathematically linked」（不同，但數學上關聯）。

圖 1.4 畫的是：Y 用 **X 的公鑰**加密，X 用 **X 的私鑰**解密。

> **方向很重要**：想寄東西給 X，就用 X 的**公鑰**加密。
> 公鑰是公開的，誰都能拿到，所以誰都能寄；但只有握著私鑰的 X 能解開。

書說公鑰密碼學讓兩件事成為可能：

1. **加密與解密** —— 兩方在不安全的管道上互傳看不懂的資料。
2. **Nonrepudiation（不可否認性）** —— 防止寄件人事後否認寄過，
   也防止資料被竄改。

### ⚠️ 書上第 2 點有兩個問題

**問題一：公鑰加密本身不提供 nonrepudiation。**
提供不可否認性的是**數位簽章**（用私鑰簽、用公鑰驗），
那是公鑰密碼學的**另一種用法**，不是加密。書把兩者混為一談了。

**問題二：「防止資料被竄改」是 integrity（完整性），不是 nonrepudiation。**
書自己在 §1.1 把這兩個列成不同的功能，這裡卻把 integrity 塞進 nonrepudiation 的描述裡。

> **記法**：加密解決「別人看不到」，簽章解決「別人改不了、且你賴不掉」。
> 兩者都用得到公私鑰，但目標不同、方向也相反。

## §1.7 digital signature、digital certificate、CA

書把這三個字連著講，因為它們是一組。

### Digital signature（數位簽章）

書的定義：一種電子簽名，可以**認證寄件人／簽署人的身分**，
並且可以確保訊息或文件的**原始內容沒被改過**。
書還說簽章「容易傳輸、無法被他人模仿、可以自動加上時間戳記」。

### Digital certificate（數位憑證）

書特別強調：**憑證和簽章是不同的東西。**

憑證是**證明「某個身分」的工具**，書打的比方很好懂 ——
它之於電子交易，就像護照或駕照之於面對面的互動。

書列出憑證裡典型包含什麼：

- 使用者名稱
- 序號
- 有效期限
- **憑證持有者的公鑰**
- **發證機構的數位簽章**（讓收件人能驗證這張憑證是真的）

> **這一條是整個 PKI 的核心**：憑證本身也是被**簽**過的。
> 你信任這張憑證，是因為你信任簽它的那個機構。

### Certification authority（CA，憑證機構）

發放並管理憑證與公鑰的機構。

### 為什麼需要憑證：把三個字串起來

⚠️ **本段不是書上的內容。** 書把三個名詞並排定義，但沒說清楚它們為什麼要湊在一起。

公鑰密碼學留了一個洞：**你怎麼知道那把「Bob 的公鑰」真的是 Bob 的？**
如果攻擊者把自己的公鑰貼上「Bob」的標籤給你，你加密後他就能解開。

憑證就是在補這個洞 —— 一個你已經信任的第三方（CA）用**它的私鑰簽**了一份文件，
內容是「這把公鑰屬於 Bob」。你用 CA 的公鑰驗證那個簽章，就能相信這個綁定關係。

**注意這是把問題往上推了一層**，不是消滅它：現在你必須先信任 CA 的公鑰。
最上層的那些（root CA）是預先裝在你的作業系統和瀏覽器裡的。

> 這條「信任鏈」在 [`linux-secure-boot-notes.md`](./linux-secure-boot-notes.md)
> 裡有從硬體開機的角度寫過一遍，可以對照著看。

## §1.8 資訊安全的五個功能

書在講完名詞後，給了一張清單。**這是本章的骨幹，要背下來。**

> 📄 **原文**　書 p.6–7 ｜ PDF p.28–29 ｜ [開啟](./cryptography-cpp.pdf#page=28)
>
> Information security basically tries to provide five types of functionalities:
> 1. Authentication　2. Authorization　3. Confidentiality or privacy
> 4. Integrity　5. Nonrepudiation

| # | 英文 | 中文 | 一句話 |
|---|---|---|---|
| 1 | **Authentication** | 認證 | **你是誰？** 驗證通訊對象的身分 |
| 2 | **Authorization** | 授權 | **你能做什麼？** 決定能不能存取某個資源 |
| 3 | **Confidentiality** | 機密性 | **別人看不到** 只有被授權的人讀得到 |
| 4 | **Integrity** | 完整性 | **別人改不了** 資料沒有被竄改 |
| 5 | **Nonrepudiation** | 不可否認性 | **你賴不掉** 事後無法否認做過 |

⚠️ **這五個跟你可能聽過的「CIA 三本柱」不一樣。**
常見的 CIA 是 Confidentiality / Integrity / **Availability（可用性）**。
**這本書的清單裡沒有 Availability**，換成了 Authentication、Authorization、
Nonrepudiation 三項。兩種分法都有人用，**讀這本書時照它的五項走**。

## §1.9 密碼學的邊界：五件事裡它只能做四件

書 §1.1 ｜ 書頁 7–9 ｜ PDF 29–31 ｜ [開啟](./cryptography-cpp.pdf#page=29)

**這一節是整章最重要的一刀。**

> 📄 **原文**　書 p.7 ｜ PDF p.29
>
> Most of the time, cryptography is associated with the ­confidentiality (or privacy)
> of information only. However, except authorization, it can offer other four
> functions of security.

換句話說：

| 功能 | 密碼學能不能提供 |
|---|---|
| Authentication | ✅ 能 |
| **Authorization** | ❌ **不能** |
| Confidentiality | ✅ 能 |
| Integrity | ✅ 能 |
| Nonrepudiation | ✅ 能 |

### 為什麼 authorization 密碼學給不了

書講得很清楚：**authorization 是作業系統或網路系統的工作**，不是密碼學的。

書的比喻是兩步驟機制：

1. **先 authentication** —— 你證明你是誰（帳號密碼、憑證）。
2. **再 authorization** —— 系統查表決定「這個身分能碰哪些資源」。

> 📄 **原文**　書 p.7 ｜ PDF p.29
>
> Authentication is a relatively stronger aspect of secu­rity than authorization,
> as it comes before authorization.

書舉的例子：公司裡所有員工都需要 authentication 才能進伺服器，
**但不是每個人都被 authorized 去用系統裡的所有資源**。

**關鍵在於**：密碼學能證明「這個請求確實來自 Alice」，
但「Alice 可不可以刪這個檔案」是一條寫在存取控制清單裡的**政策**，
跟數學無關。密碼學把身分送到門口，開不開門是別人的事。

> ⚠️ **這是初學者最常搞混的地方，也是這章最值得記住的一句話：**
> **密碼學回答「你是誰」，不回答「你可以做什麼」。**

### 其餘四項書怎麼說

- **Authentication**：驗證在網路上通訊的實體身分。書強調**沒有認證的話，
  任何有網路存取權的人都能用現成工具偽造來源 IP、冒充他人**。
- **Confidentiality**：確保只有被授權的使用者能讀。沒有它，
  任何有網路存取權的人都能用現成工具竊聽流量、攔截有價值的資訊。
- **Integrity**：資料沒有被竄改。
- **Nonrepudiation**：書花最多篇幅講這個。核心是**證據**——

> 📄 **原文**　書 p.9 ｜ PDF p.31 ｜ [開啟](./cryptography-cpp.pdf#page=31)
>
> [...] systems must provide evidence of communications and transactions that
> should involve the identities or credentials of each party so that it is
> impos­sible to refute the evidence.

書給的具體做法：郵件系統加上**時間戳記**，並用寄件人的**數位簽章**簽署訊息。
因為訊息裡有時間戳和獨一無二的簽章，寄件人事後否認的話，
那個謊很容易被戳破。收件端也可以用**簽了名的收件回執**達成同樣效果。

## §1.10 密碼學不能做的事

書 §1.2 ｜ 書頁 9–10 ｜ PDF 31–32 ｜ [開啟](./cryptography-cpp.pdf#page=31)

書用一整節提醒：**密碼學只是整體安全的一部分。**

### 最弱環節原則

> 📄 **原文**　書 p.10 ｜ PDF p.32 ｜ [開啟](./cryptography-cpp.pdf#page=32)
>
> security depends on the appropriate protection mechanism of the weakest link in
> the entire security system.

書給了兩個很具體的例子：

**例子一：紙本。** 一家公司可以裝上最好的密碼技術，
但如果有人（入侵者或員工）**可以直接走進辦公室，拿走印成明文的紙本資料**，
所有的保護努力全部崩塌。

**例子二：傳輸加密但儲存明文。** 你把資料加密後傳過網路來保護機密性，
**卻在寄件端或收件端的電腦上以明文儲存** —— 這仍然是有漏洞的狀態。
書建議那些電腦也必須被保護（資料也存成加密格式、加上存取密碼），
而且整個網路要有強固的防火牆並放在安全的設施裡。

**書明講最後這些工作「不是密碼學或密碼技術的事」。**

### 書列出的其他決定因素

整體安全強度取決於：

- 技術本身是否**適用**（suitability of the technology）
- **足夠的安全程序與流程**（adequate security procedures and processes）
- **人有多會用**這些程序、流程與技術（how well people use them）

> **注意第三項。** 這是本章唯一一次提到「人」。
> 你會在第 3 章看到這句話應驗 —— Enigma 沒有被數學破解，
> 是被**德軍操作員習慣用 AAA、ABC 這種偷懶的訊息金鑰**破解的。

## ⚠️ 第 1 章的過時陳述與缺口

### 錯誤或會誤導的陳述

| 位置 | 書上怎麼寫 | 問題 |
|---|---|---|
| 書 p.3 | 串流密碼「現代不太用了」 | **錯**。ChaCha20 是今天 TLS 1.3 的主力之一，見 §1.3 |
| 書 p.3 | 金鑰「有時就是指要遵循的步驟或規則」 | 跟它自己的正式定義矛盾，違反 Kerckhoffs 原則，見 §1.2 |
| 書 p.4 | cryptosystem =「一對演算法 + 金鑰」 | 少了 **KeyGen**，見 §1.5 |
| 書 p.5–6 | Nonrepudiation 被列為公鑰**加密**的功能，且描述裡混進 integrity | 提供不可否認性的是**簽章**不是加密，見 §1.6 |

### 這章（乃至全書）沒有的東西

| 缺什麼 | 為什麼要緊 |
|---|---|
| **MAC / HMAC** | 全書只出現 2 次。**Integrity 這條線在書裡是斷的** —— 只有 hash（第 10、11 章），沒有帶金鑰的訊息認證碼。而 hash 本身**不提供** integrity（攻擊者可以連 hash 一起換掉） |
| **AEAD** | AEAD 全書 0 次、ChaCha 0 次。今天做對稱加密的**預設形態**就是 AEAD（同時給機密性和完整性），書裡等於不存在 |
| **CSPRNG** | 無專章。§1.5 說過，這是現實中最常出事的地方，第 3 章就會撞到 |
| **Availability** | 五項清單裡沒有可用性；DoS 這類攻擊不在本書視野內 |
| **Kerckhoffs 原則** | 沒有提到這個名字，但它是全書的隱含前提 |

## 📌 第 1 章的三句話重點

1. **演算法公開、金鑰保密** —— 安全性只能來自金鑰，這是後面十章的共同前提。
2. **密碼學回答「你是誰」，不回答「你可以做什麼」** ——
   五個安全功能裡，唯獨 authorization 它給不了。
3. **密碼學是整體安全的一部分，不是全部** ——
   整條鏈的強度由最弱的一環決定，而最弱的那環經常是人或紙。

## 📖 第 1 章名詞小抄

| 英文 | 中文 | 一句話 |
|---|---|---|
| Plaintext / Cleartext | 明文 | 本來想傳的訊息 |
| Ciphertext | 密文 | 加密後的結果 |
| Encryption / Decryption | 加密／解密 | 明文↔密文的過程 |
| Cipher / Cryptoalgorithm | 密碼演算法 | 執行加解密的那套明確步驟 |
| Key | 金鑰 | 決定演算法輸出的那個秘密參數 |
| Stream cipher | 串流密碼 | 一次處理一個 bit／byte |
| Block cipher | 區塊密碼 | 一次處理一整塊（如 64 bits） |
| Key stream | 金鑰流 | 串流密碼中由金鑰產生、與明文混合的位元流 |
| CFB (Cipher Feedback) | 密文回饋 | 把前一個密文區塊混進下一個明文區塊 |
| Cryptology | 密碼學（廣義） | 傘狀名詞，含編碼學與分析學 |
| Cryptography | 密碼編碼學 | 怎麼造 |
| Cryptanalysis | 密碼分析學 | 怎麼破 |
| Cryptosystem | 密碼系統 | 加密＋解密演算法＋金鑰（⚠️ 標準定義還要加 KeyGen） |
| Symmetric cryptography | 對稱式密碼學 | 加解密同一把金鑰 |
| Public-key / Asymmetric | 公開金鑰／非對稱 | 公鑰加密、私鑰解密，兩者數學關聯 |
| Digital signature | 數位簽章 | 用私鑰簽，證明身分且內容未被竄改 |
| Digital certificate | 數位憑證 | 由 CA 簽署，綁定「某把公鑰屬於某個身分」 |
| Certification authority (CA) | 憑證機構 | 發放並管理憑證與公鑰的機構 |
| Authentication | 認證 | 你是誰 |
| Authorization | 授權 | 你能做什麼（⚠️ 密碼學給不了） |
| Confidentiality / Privacy | 機密性 | 別人看不到 |
| Integrity | 完整性 | 別人改不了 |
| Nonrepudiation | 不可否認性 | 你賴不掉 |

---
---

# 第 2 章 古典密碼演算法

**Classical Cryptographic Algorithms** ｜ 作者 Sheikh Shaugat Abdullah、Saiful Azad
書頁 11–34 ｜ PDF 33–56 ｜ [開啟](./cryptography-cpp.pdf#page=33)

> 四個古典密碼，每個都照「**演算法 → 實作 → 為什麼會被破**」走一遍。
> 書的體例在這章最整齊。

## §2.0 這章在解什麼問題

在電腦出現之前，人怎麼加密。

但這章真正的價值不在那四個古典密碼本身（它們今天沒有任何實用價值），
而在於**它們是怎麼一個接一個被破掉的** —— 每一個新密碼都是在修補前一個的漏洞，
而每一次修補又留下新的漏洞。**這條軍備競賽的路線一路通到第 4～6 章的現代區塊密碼。**

讀這章的正確方式：**每一節先讀 Limitations（為什麼會被破），再回頭讀演算法。**

## §2.1 Caesar Cipher（凱撒位移密碼）

書頁 12–15 ｜ PDF 34–37 ｜ [開啟](./cryptography-cpp.pdf#page=34)

以 Julius Caesar 命名，他在軍事行動中用過。書說他把每個字母換成
**字母表往後三位**的那個字母。書稱它是「有紀錄以來第一次為了保護訊息而使用加密」。

它屬於 **substitution cipher（替換式密碼）**：
每個字母被換成距離它固定距離的另一個字母，走到 Z 就繞回開頭。

### §2.1.1 演算法：把字母當數字，加上一個位移

書 §2.1.1 給了四個步驟：

> 📄 **原文**　書 p.12 ｜ PDF p.34
>
> Step 0: Mathematically, map the letters to numbers (i.e., A = 1, B = 2, and so on).
> Step 1: Select an integer key K in between 1 and 25 [...]
> Step 2: The encryption formula is "Add k mod 26"; that is, the original letter L
> becomes (L + k)%26.
> Step 3: The deciphering is "Subtract k mod 26"; that is, the encrypted letter L
> becomes (L – k)%26.

書上表 2.1 給了 key = 3 的完整對照表：A→d、B→e、…、X→a、Y→b、Z→c。

#### 就地補：什麼是 mod（模運算）

⚠️ **本段不是書上的內容。**

`a % n`（唸作 a mod n）就是 **a 除以 n 之後的餘數**。

```
17 % 5 = 2      因為 17 = 3×5 + 2
26 % 26 = 0
27 % 26 = 1
```

**它在密碼學裡的用途永遠是同一個：把一個會越加越大的數字，圈回一個固定的範圍內。**

字母表只有 26 個位置。如果 Y（第 24 位，從 0 算）加上位移 3，得到 27 ——
字母表沒有第 27 位。`27 % 26 = 1`，繞回到 B。

**把字母表想成一個時鐘**，只是它有 26 格而不是 12 格。加密就是把指針往前撥 k 格，
解密就是往回撥 k 格。撥過頭就自動繞圈 —— 這就是 mod 在做的事。

> 這個「繞圈」的想法你會在這本書裡看到幾十次。
> 第 8 章的 RSA、第 9 章的 ECC，整套數學都建立在模運算上，
> 只是那時候的模數不是 26，而是幾百位數的大質數。

#### 解密為什麼要多加一個 26

書 Step 3 寫的是 `(L – k) % 26`。**這在數學上對，在 C++ 裡會出事。**

C++ 的 `%` 對負數的結果是**負的**：`(2 - 5) % 26` 在 C++ 裡等於 `-3`，不是 `23`。

所以實作時必須先把它加回正數範圍：`((L - k + 26) % 26)`。
**書上的程式碼確實這樣做了**（見下一節），但書上的**演算法描述沒有提**。
這是本章第一個「演算法跟程式碼對不起來」的地方，而且是**程式碼對、描述不夠**。

#### 金鑰空間有多大

書說 key 取 1 到 25。**為什麼不是 0 到 25？**
因為 key = 0 等於不加密（每個字母對到自己），沒有意義。同理 key = 26 也等於不加密。

所以**總共只有 25 把有效的金鑰**。記住這個數字，下一節就會用到。

### §2.1.2 💻 程式碼對照

書 §2.1.2 ｜ 書頁 13–14 ｜ PDF 35–36 ｜ [開啟](./cryptography-cpp.pdf#page=35)

核心就是一個函式。**以下照書原樣轉錄**（含書上的排版錯誤）：

```cpp
charcaesar(char c, int k)//'c' holds the letter to be
   encrypted or decrypted and 'k' holds the key
{
if(isalpha(c) && c ! = toupper(c))
   {
      c = toupper(c);//use upper to keep from having
          to use two separate for A..Z a..z
      c = (((c-65)+k)% 26) + 65; //Encryption, (add k
          with c) mod 26
   }
else
   {
      c = ((((c-65)-k) + 26)% 26) + 65; //Decryption,
          (subtract k from c) mod 26
      c = tolower(c);//use lower to keep from having
          to use two separate for A..Z a..z
   }
return c;
}
```

> ⚠️ **正確寫法**：`char caesar(...)`、`c != toupper(c)`。
> 書上印的 `charcaesar` 和 `! =` 不能編譯，原因見本筆記開頭。

#### 一行一行對回演算法

| 程式碼 | 對應演算法的哪一步 |
|---|---|
| `c - 65` | **Step 0** 把字母映射成數字。65 是 `'A'` 的 ASCII 碼，所以 `'A'-65 = 0`、`'B'-65 = 1` |
| `+ k` | **Step 2** 加上金鑰 |
| `% 26` | 繞回 26 個字母的範圍內 |
| `+ 65` | 把數字轉回 ASCII 字元 |
| `(((c-65)-k) + 26) % 26` | **Step 3** 解密。注意那個 `+ 26` —— 就是上一節說的、避免 C++ 負數取餘的修正 |

**整個凱撒密碼就是這兩行算式。** 這也說明了為什麼它這麼容易破。

### §2.1.3 ⚠️ 書上的演算法跟書上的程式碼對不起來

**這一節是本章最值得花時間的地方。** 書的 §2.1.1（演算法）和 §2.1.2（程式碼）
之間至少有三處矛盾，而且書完全沒有說明。

#### 落差一：A = 1 還是 A = 0

| | 說什麼 |
|---|---|
| **演算法 Step 0** | `A = 1, B = 2, and so on` |
| **程式碼** | `c - 65`，而 `'A'` 的 ASCII 是 65，所以 **A = 0** |

**哪個對？程式碼對。**

如果真的用 A = 1，那 Z = 26，而 `26 % 26 = 0` —— **對應不到任何字母**
（因為 1 到 26 才是有效範圍，0 不是）。**書上的演算法描述會在字母 Z 上壞掉。**

用 A = 0（Z = 25）就沒有這個問題：所有結果都落在 0–25，剛好對應 26 個字母。

> **這就是「程式碼當觀念的驗證」的價值。** 光讀 Step 0 你不會發現有問題；
> 對照程式碼才看得出書的數學描述有 off-by-one 的瑕疵。

#### 落差二：金鑰上限是 25 還是 26

| | 說什麼 |
|---|---|
| **演算法 Step 1** | `Select an integer key K in between 1 and 25` |
| **程式碼（`main`）** | `if (key < 1 \|\| key > 26) throw "Incorrect key"` — **放行 26** |
| **程式碼的提示字串** | `"Choose key value (choose a number between 1 to 26): "` |

**演算法對，程式碼錯。** key = 26 時 `(c-65+26) % 26 = (c-65) % 26`，
**輸出等於輸入，完全沒有加密**。程式碼卻讓你選它。

不是安全漏洞（這東西本來就沒有安全性），但它是個真的 bug。

#### 落差三：程式碼偷偷用「大小寫」決定要加密還是解密

**這一條演算法完全沒提。**

看那個 `if` 條件：

```cpp
if(isalpha(c) && c ! = toupper(c))
```

`c != toupper(c)` 的意思是「c 跟它的大寫版本不同」，也就是 **c 是小寫字母**。

所以這份實作的實際行為是：

- **輸入小寫** → 走 `if` 分支 → **加密**，輸出大寫
- **輸入大寫** → 走 `else` 分支 → **解密**，輸出小寫

`main` 裡的提示也證實了這件事：

> 📄 **原文**　書 p.14 ｜ PDF p.36 ｜ [開啟](./cryptography-cpp.pdf#page=36)
>
> NOTE: Put LOWER CASE letters for encryption and
> UPPER CASE letters for decryption

**這不是凱撒密碼的一部分。** 大小寫在真正的凱撒密碼裡沒有任何意義 ——
這純粹是這個 demo 程式為了用一個函式同時做加解密，而發明的**介面設計**。

⚠️ **為什麼這件事要緊**：初學者對照程式碼學演算法時，
很容易把這種「實作方便」的設計誤認為演算法的一部分。
**要能分辨哪些是密碼學，哪些只是這支程式的 UI。**

#### 順帶：其他小問題

- `#include <stdlib.h>` 有，但 `isalpha`、`toupper`、`tolower` 需要的是 `<cctype>`。
- 提示字串 `"Enter cipertext"` 拼錯了（應為 ciphertext），而且加密時也顯示這句。
- 非字母字元（空格、標點）會走進 `else` 分支被當成密文處理，輸出亂碼。

### §2.1.4 為什麼會被破

書 §2.1.3 ｜ 書頁 15 ｜ PDF 37 ｜ [開啟](./cryptography-cpp.pdf#page=37)

書先講了一個有趣的歷史理由：

> 📄 **原文**　書 p.15 ｜ PDF p.37
>
> The Caesar cipher was reasonably secure in earlier days (until the ninth century)
> because most of the enemies of Julius Caesar were illiterate.

**當年它的安全性來自敵人不識字** —— 他們以為那是某種外國語言。
這其實是個很好的提醒：**安全性從來不是絕對的，它取決於攻擊者有什麼能力。**

書給了兩種破法：

#### 破法一：Brute force（暴力破解）

**只有 25 種可能的金鑰。** 全部試一遍，看哪一個結果是有意義的單字。
找到金鑰之後，整段密文都能正確還原。

> 一個 `for` 迴圈跑 25 次就結束了。**這就是為什麼金鑰空間的大小是安全性的第一道門檻。**

#### 破法二：Frequency analysis（頻率分析）

書說這個方法「比暴力破解更聰明也更快」，細節留到 §2.2.3 才展開。

⚠️ **書漏了一個更根本的問題。** 就算金鑰空間變大，
凱撒密碼還有一個致命特性：**同一個明文字母永遠對應到同一個密文字母**。
這叫**保留了頻率分佈**，是下一節被破的原因，也是整章的主線。

## §2.2 Monoalphabetic Cipher（單字母替換密碼）

書頁 15–19 ｜ PDF 37–41 ｜ [開啟](./cryptography-cpp.pdf#page=37)

**凱撒密碼的直接升級：不再只是「整體位移 k 格」，而是一張完全任意的替換表。**

書上表 2.2 給了範例：A→q、B→w、C→e、D→r…（就是鍵盤上的 qwerty 順序）。

mono 是「一」的意思 —— 每個明文字母**一對一**映射到單一個密文字母。

### §2.2.1 演算法：不再只是位移，而是整張替換表

書 §2.2.1 三個步驟：

> 📄 **原文**　書 p.15 ｜ PDF p.37
>
> Step 0: Generate plaintext–ciphertext pair by mapping each plaintext letter to a
> different random ciphertext letter.
> Step 1: To encipher, for each letter in the original text, replace the plaintext
> letter with a ciphertext letter.
> Step 2: For deciphering, reverse the procedure in step 1.

#### 金鑰空間爆炸性成長

凱撒密碼的金鑰是**一個數字**（25 種選擇）。
單字母替換的金鑰是**一整張表** —— 也就是 26 個字母的一種**排列（permutation）**。

有多少種排列？**26! = 403,291,461,126,605,635,584,000,000**（約 4×10²⁶）。

書因此說它「secure against brute-force attack」（能抵抗暴力破解）——
**這句話是對的**。就算一秒試一兆種，也要跑一千萬年以上。

#### ⚠️ 書的措辭在這裡很混亂

> 📄 **原文**　書 p.15 ｜ PDF p.37
>
> Unlike Caesar cipher, this technique uses a random key for every single letter
> (i.e., total of 26 keys).

**「26 把金鑰」這個說法是錯的，或至少嚴重誤導。**

正確的理解是：**只有一把金鑰**，那把金鑰**是一個 26 個字母的排列**。
金鑰空間是 26!，不是 26。

如果真的是「26 把獨立的金鑰」，那金鑰空間會是 26²⁶ ——
那是允許重複的情況（兩個明文字母可以對到同一個密文字母），
**那樣就不可逆了，根本無法解密**。所以它必須是排列，必須一對一。

> **記住結論就好：一把金鑰 = 一張一對一的替換表，金鑰空間 26!。**

### §2.2.2 💻 程式碼對照

書 §2.2.2 ｜ 書頁 16–18 ｜ PDF 38–40 ｜ [開啟](./cryptography-cpp.pdf#page=38)

程式用兩個 `vector<char>` 存那張表：`Plain` 和 `Cipher`，同一個索引互相對應。

`PutCharInVec()` 負責產生這張表。**以下照書原樣轉錄關鍵片段**：

```cpp
for(inti = 0; i< 26; i++) {
Plain.push_back(i+97); //Assigning the plain
characters in Vector
  }
...
bool exist;
intnum;
for(inti = 0; i< 26; i++) {
  // Generating unique random numbers as keys
while (exist) {
exist = false;
num = rand()% 26 + 1;
for (vector <char> :: iterator it = Cipher.begin(); it
! = Cipher.end(); it++) {
if ((*it) = = num) {
exist = true;
break;
           }
       }
    }
Cipher.push_back(((i + num)% 26) + 65);
  }
```

`Plain` 填的是 `i+97`，即小寫 `'a'`～`'z'`。`Cipher` 填的是 `+65`，即大寫。

加解密就是查表：

```cpp
charMonoalphabetic (char c)
{
  //Encryption
if (c ! = toupper(c)) {
for (inti = 0; i< 26; i++) {
if (Plain[i] = = c) {
return Cipher[i];
       }
     }
   }
  //Decryption
else { ... if (Cipher[i] = = c) { return Plain[i]; } ... }
```

**跟凱撒一樣，還是用大小寫決定加密還是解密。**（同 §2.1.3 落差三）

### §2.2.3 ⚠️ 這段程式碼產生的根本不是隨機替換表

**這是我在整章裡發現最嚴重的問題，而且書完全沒有察覺。**

⚠️ **本節是我對書上程式碼的逐行推導。依 brief 規定，本輪不編譯不執行，
以下結論來自閱讀而非實測。**

逐行追 `PutCharInVec()` 那個迴圈：

**第 1 圈（i = 0）**
`exist` 是**未初始化**的 `bool`。假設它的垃圾值是 true：

- 進入 `while` → `exist = false` → `num = rand()%26 + 1`（產生一個 1～26 的數）
- 內層 `for` 掃 `Cipher`，此時 `Cipher` 是**空的**，掃不到東西，`exist` 維持 false
- `while` 條件為 false → **離開迴圈**
- `Cipher.push_back(((0 + num) % 26) + 65)`

**第 2 圈（i = 1）**
`exist` 現在是 **false** → `while (exist)` **整個被跳過** → **`num` 不會重新產生**

**第 3 到 26 圈**：同上，`while` 永遠不會再執行。

#### 結論

`num` **只在第一圈被賦值一次，之後固定不變**。所以整張表是：

```
Cipher[i] = ((i + num) % 26) + 65
```

**這是一個位移量為 num 的凱撒密碼。**

也就是說 —— 這段號稱產生「26! 種可能的隨機替換表」的程式碼，
**實際上產生的是一張凱撒位移表，金鑰空間只有 26**。
正是上一節（§2.1.4）才剛說過「一個 for 迴圈就破得掉」的那個東西。

#### 就算 while 迴圈有跑，去重檢查也是壞的

```cpp
if ((*it) = = num)
```

`*it` 是 `Cipher` 裡存的 `char`，值域是 **65～90**（大寫字母的 ASCII）。
`num` 的值域是 **1～26**。

**兩者永遠不可能相等。** 這個去重檢查不管怎樣都不會偵測到重複。

#### 還有一個未定義行為

如果 `exist` 的垃圾值剛好是 **false**，`while` 從第一圈就不會執行，
`num` **從頭到尾都是未初始化的**。讀取未初始化變數在 C++ 裡是
**undefined behavior（未定義行為）** —— 程式可能輸出任何東西。

#### 為什麼這件事對初學者特別重要

> **書的文字說這個密碼能抵抗暴力破解（正確），
> 書的程式碼卻做出一個 25 秒就能暴力破解的東西（錯誤），
> 而書把兩者並排放在同一節裡，沒有任何提示。**

如果你只讀文字，你學到正確的觀念但不知道實作有多容易搞砸。
如果你只抄程式碼，你會以為自己實作了一個安全的東西。

**這正是「程式碼當觀念的驗證」要防的事** ——
把兩邊對起來讀，才會發現它們沒對上。

⚠️ **依 brief，本輪不改寫成正確版本。** 但要知道正確做法是什麼：
產生一個真正的排列（例如 Fisher–Yates shuffle），並且用**密碼學安全的亂數源**
（不是 `rand()`）。書全書沒有 CSPRNG 的討論，見第 1 章結尾的缺口表。

### §2.2.4 為什麼會被破

書 §2.2.3 ｜ 書頁 18–19 ｜ PDF 40–41 ｜ [開啟](./cryptography-cpp.pdf#page=40)

書給了兩個缺點。

#### 缺點一：人記不住

金鑰是 26 個字母的隨機順序，**很難記**，手動加解密既費時又容易出錯。
（這是實務上的問題，不是數學上的。）

#### 缺點二：頻率分析 —— 這才是致命傷

> 📄 **原文**　書 p.18–19 ｜ PDF p.40–41
>
> monoalphabetic substitution is vulner­able to frequency analysis because it does
> not change the relative letter frequencies.

**關鍵句是 "does not change the relative letter frequencies"（沒有改變字母的相對頻率）。**

書的推理鏈：

1. **人類語言不是隨機的。** 書舉例：`e` 和 `t` 出現得最頻繁；
   `the`、`and`、`a`、`an` 這些字非常常見。
2. 因為是一對一固定映射，**明文裡最常出現的字母，在密文裡也是最常出現的**。
3. 所以：統計密文裡每個字母的出現頻率，
   拿去跟標準英文字母頻率比對，就能猜出映射關係。
4. 書說有時需要 **backtracking（回溯）** 來確認猜測。

#### 為什麼 26! 那麼大還是沒用

⚠️ **本段不是書上的內容，但這是本章最重要的一個觀念。**

**金鑰空間大 ≠ 安全。**

暴力破解要試 4×10²⁶ 種可能；但頻率分析**根本不試金鑰** ——
它直接從密文的統計特性反推出映射表，一次只需要解決 26 個字母的對應關係，
而且每猜對一個都會讓其他的更好猜。

> **這是整個密碼學裡最重要的教訓之一：
> 攻擊者不會照你設計的方式來攻擊。**
> 你把門鎖加固到 4×10²⁶ 種鑰匙，他從窗戶進來。

#### 書指出的解法方向

> 📄 **原文**　書 p.19 ｜ PDF p.41
>
> To improve the security of monoalphabetic cipher, multiple cipher­text letters
> need to be mapped with each corresponding plaintext letter. This technique is
> called polyalphabetic cipher.

**讓一個明文字母可以對到多個不同的密文字母** —— 那樣頻率就被打散了。
這就是 §2.4 的主題。

（但書在中間先插了 §2.3 Playfair，走的是另一條路：**一次加密兩個字母**。）

## §2.3 Playfair Cipher

書頁 19–27 ｜ PDF 41–49 ｜ [開啟](./cryptography-cpp.pdf#page=41)

**另一條升級路線：不改變「一對一」，而是改變「一次處理幾個字母」。**

書的歷史說明：1854 年由 **Charles Wheatstone** 發明，
但以推廣它的朋友 **Lord Playfair** 命名。
英軍在第二次波耳戰爭與第一次世界大戰中大量使用，
澳洲軍隊在二戰中也用於戰術用途。

### §2.3.1 演算法：5×5 矩陣與雙字母加密

它是 **digraph substitution cipher（雙字母替換密碼）**——
一次加密**一對**字母，而不是單一字母。

書的關鍵論證：

> 📄 **原文**　書 p.19 ｜ PDF p.41
>
> It is equivalent to a monoalphabetic cipher with a set of 25 × 25 = 625
> characters (i.e., for each possible pair) for the English language.

也就是說：**把「字母對」當成新的字母，那字母表就從 26 個變成 625 個。**
頻率分析要對付 625 種符號，難度大幅提高。

#### 為什麼是 25 不是 26

**I 和 J 被合併成同一格。** 5×5 的矩陣只有 25 格，英文有 26 個字母，
所以必須犧牲一個。書選擇把 I 和 J 放在同一格（書上表 2.3 寫成 `I/J`）。

#### 建矩陣：書 Step 0～2

> 📄 **原文**　書 p.19–20 ｜ PDF p.41–42
>
> Step 0: Select the character key. The maximum size of the key is 25, and it can
> only be letters.
> Step 1: Identify double letters in the key and count them as one.
> Step 2: Set the 5 × 5 matrix by filling the first positions with the key. Fill the
> rest of the matrix with other letters.

流程：**金鑰去重 → 從左上角開始填進矩陣 → 剩下的格子用沒用過的字母按順序補完。**

書上表 2.3 用金鑰 `simple` 示範：

|   |   |   |   |   |
|---|---|---|---|---|
| S | I/J | M | P | L |
| E | A | B | C | D |
| F | G | H | K | N |
| O | Q | R | T | U |
| V | W | X | Y | Z |

前六格是 `S I M P L E`（金鑰，無重複），
之後從 A 開始把沒用到的字母依序填入（A B C D F G H K N O Q R T U V W X Y Z），
J 跳過（跟 I 同格）。

#### 處理明文：書 Step 3～4

- **Step 3**：找出**成對的重複字母**，把後面那個換成 `x`。
  書的例子：`killer` → `kilxer`（`ll` 變成 `lx`）。
- **Step 4**：明文兩個一組加密。**如果總長度是奇數，在結尾補一個 `x` 湊成偶數。**

> **為什麼要處理重複字母？** 因為 Step 5 的三條規則中，
> 如果一對是同樣的兩個字母（例如 `LL`），它們在矩陣裡是同一格，
> 「同列往右」跟「同行往下」會產生矛盾的結果。所以必須先拆開。

#### 加密規則：書 Step 5 的三種情況

對每一對字母，看它們在 5×5 矩陣裡的相對位置：

| 情況 | 規則 |
|---|---|
| **1. 同一列（row）** | 各自換成**它右邊**的那個字母，走到最右邊就繞回最左邊 |
| **2. 同一行（column）** | 各自換成**它下面**的那個字母，走到最下面就繞回最上面 |
| **3. 其他（構成矩形）** | 各自換成**同一列、但在對方那一行**的字母 |

情況 3 最不直覺：兩個字母構成一個矩形的兩個對角，
**輸出就是另外兩個對角**（保持各自原來的列）。

**解密（Step 6）**：反向做 Step 5、Step 4、Step 3
—— 同列往**左**、同行往**上**、矩形規則不變（它自己是對稱的）。

### §2.3.2 💻 程式碼對照

書 §2.3.2 ｜ 書頁 20–26 ｜ PDF 42–48 ｜ [開啟](./cryptography-cpp.pdf#page=42)

**本章最長的實作（7 頁）**，而且是唯一用 class 寫的。

`class PlayFair` 的成員函式分工很清楚：

| 函式 | 對應演算法哪一步 |
|---|---|
| `keyWithoutDuplicateAlphabet()` | **Step 1** 金鑰去重 |
| `setMatrix()` | **Step 0、2** 建 5×5 矩陣 |
| `findRow()` / `findCol()` | 查一個字母在矩陣的位置 |
| `encrypt()` | **Step 3、4、5** |
| `decrypt()` | **Step 6** |

#### 三條規則怎麼寫成程式

`encrypt()` 的核心是一個三分支判斷。**照書原樣轉錄**：

```cpp
	//for the letter pair falls in the same row if
  (findRow(str[i]) = = findRow(str[i+1])) {
	output.push_back(matrix[findRow(str[i])]
  [(findCol(str[i]) + 1)% 5]);
	output.push_back(matrix[findRow(str[i + 1])]
  [(findCol(str[i + 1]) + 1)% 5]);
  }
	//for the letter pair falls in the same
  column
	else if (findCol(str[i]) = =
  findCol(str[i+1])) {
	output.push_back(matrix[(findRow(str[i])
  + 1)% 5][findCol(str[i])]);
	...
  }
   //for other cases
  else {
	output.push_back(matrix[findRow(str[i])]
  [findCol(str[i + 1])]);
	output.push_back(matrix[findRow(str[i + 1])]
  [findCol(str[i])]);
  }
```

**這三段跟 Step 5 的三條規則一一對應，而且寫得很漂亮**：

- **同列**：列不變，行 `(col + 1) % 5` —— 那個 `% 5` 就是「繞回最左邊」。
- **同行**：行不變，列 `(row + 1) % 5` —— 繞回最上面。
- **矩形**：`matrix[自己的列][對方的行]` —— **一行程式碼就是規則 3 的定義。**

> 又是 mod 在做繞圈。這次模數是 5（矩陣邊長），不是 26。
> **同一個工具，換一個範圍。**

#### 為什麼 I/J 合併在程式裡看得到

```cpp
	if (ch = = 'J') alphabet_exist = true;//since
  i and j both co-exist in the same cell, we'll
  only put i in the cell
```

填矩陣時把 J 標記成「已存在」，它就永遠不會被填進去 —— I 佔了那格。

查詢時則反過來把 J 折回 I：

```cpp
if (ch = = 'j') ch = 'i';
```

### §2.3.3 ⚠️ 這份實作的三個問題

⚠️ **本節是我對書上程式碼的逐行推導，未經編譯執行。**

#### 問題一：Step 4 根本沒有實作

書 Step 4 說「如果明文長度是奇數，在結尾補一個 `x`」。**程式碼沒有這樣做。**

主迴圈是：

```cpp
for (inti = 0; i<str.length(); i = i + 2) {
```

長度是奇數時，最後一圈 `i = length-1`，而迴圈裡會存取 `str[i+1]`，
也就是 **`str[length]`** —— 那是字串結尾的 `'\0'`。
`findRow('\0')` 會回傳 `-1`（書上的 `return -1; //If not found`），
接著 `matrix[-1][...]` 就是**陣列越界，未定義行為**。

程式碼在迴圈結束後做了一件很奇怪的事：

```cpp
if ((str.length()% 2) ! = 0) {
           output[output.length() - 1] =
toupper(str[str.length() - 1]);
     }
```

**把輸出的最後一個字元覆寫成明文的最後一個字母。**
也就是說 —— 奇數長度時，**最後一個字母以明文原樣留在密文裡**。

這既不符合 Step 4，也是個真實的資訊洩漏。

#### 問題二：解密時把所有的 X 都刪掉

```cpp
for (inti = 0; i<output.length(); i++) {
          if (output[i] = = 'X') {
          output.erase(output.begin() + i);
          }
   }
```

書 Step 6 說解密要「反向做 Step 3」，也就是把加密時插入的 `x` 拿掉。
**但程式碼刪的是所有的 X，包括明文裡本來就有的 X。**

`box` 加密再解密會變成 `bo`。

而且還有第二個 bug：`erase` 之後 `i++` 照常執行，
**會跳過剛剛被往前移動的那個字元**。連續兩個 X 只會刪掉一個。

⚠️ **這個問題沒有乾淨的解法** —— 這是 Playfair 演算法本身的性質，
不是實作的疏忽。解密端無法區分「這個 x 是填充的」還是「本來就有的」。
實務上的處理是靠人讀出來判斷。**書沒有討論這件事。**

#### 問題三：插入 x 的迴圈會錯位

```cpp
for (inti = 1; i<str.length(); i = i + 2) {
      if (str[i-1] = = str[i]) {
      ...
      str = temp1 + 'x' + temp2;
      }
}
```

插入 `x` 之後字串**變長了**，但迴圈的索引 `i` 還是照 `+2` 往前走 ——
**插入點之後的所有配對都會錯開一格**，重複字母的偵測從此失效。

例如 `aabb`：i=1 時偵測到 `aa`，插入變成 `axabb`（長度 5）；
i=3 時比較的是 `str[2]='a'` 和 `str[3]='b'`，不相等 —— **`bb` 被漏掉了**。

### §2.3.4 為什麼會被破

書 §2.3.3 ｜ 書頁 27 ｜ PDF 49 ｜ [開啟](./cryptography-cpp.pdf#page=49)

> 📄 **原文**　書 p.27 ｜ PDF p.49
>
> Even though Playfair is considerably complicated to break, it is still vulnerable
> to frequency analysis because it leaves some ­formation of plaintext intact.

**還是頻率分析，只是變難了。**

書的說法：現在要分析的是 **625 種可能的雙字母組（digraph）**，
而不是 25 種單字母。所以**需要大量的密文**才能做出可靠的統計。

書指出最簡單的實際破法**不是**統計：

> 📄 **原文**　書 p.27 ｜ PDF p.49
>
> assuming some of the words from the plaintext using the knowledge of area, time,
> or context of the message can be helpful for retrieving the key, and so far this
> is the simplest way to crack this cipher.

**用情境知識猜出明文裡的某些字**（地名、時間、上下文），
然後反推金鑰。這是 **known-plaintext attack（已知明文攻擊）** 的雛形。

> ⚠️ 書沒有用 "known-plaintext attack" 這個術語，但這正是它描述的東西。
> **記住這個名詞** —— 它在第 3 章破解 Enigma 時會再出現一次，
> 而且是決定性的。

## §2.4 Polyalphabetic Cipher（多字母替換密碼／Vigenère）

書頁 27–34 ｜ PDF 49–56 ｜ [開啟](./cryptography-cpp.pdf#page=49)

回到 §2.2.4 書指出的那條路線：**讓同一個明文字母能對到不同的密文字母。**

書的定義很精準：

> 📄 **原文**　書 p.27 ｜ PDF p.49
>
> the polyalphabetic cipher uses a collection of standard Caesar ciphers.

**它就是一堆凱撒密碼輪流用。**

歷史：1467 年 **Leon Battista Alberti** 的 Alberti cipher 是第一個多字母密碼。
書說最有名的特例是 **Vigenère cipher**。

### §2.4.1 演算法：用一把金鑰輪流切換多張替換表

書 §2.4.1 的四個步驟很短：

> 📄 **原文**　書 p.29 ｜ PDF p.51
>
> Step 0: Select a multiple-letter key.
> Step 1: To encrypt, the first letter of the key encrypts the first l­etter of the
> plaintext, the second letter of the key encrypts the second letter [...]
> Step 2: W hen all letters of the key are used, start over with the first letter.
> Step 3: The decryption process is the reverse of step 1. The ­number of letters in
> the key determines the period of the cipher.

**金鑰不再是一個數字，而是一個單字。** 金鑰的每個字母決定該位置要用哪一個位移。
金鑰用完就從頭再來。

#### 書的範例（表 2.4），金鑰 `run`

```
Plaintext  t o b e o r n o t t o b e t h a t i s t h e
Key        r u n r u n r u n r u n r u n r u n r u n r
Cipher     K I O V I E E I G K I O V N U R N V J N U V
```

金鑰 `run` 只有三個字母，所以它一直重複：`run run run run…`

#### Vigenère table（tabula recta）

書上表 2.5 給了一張 26×26 的表：第一列是 A~Z，
第二列從 B 開始（B C D…Z A），第三列從 C 開始，以此類推 ——
**每一列就是一個位移量不同的凱撒密碼**。

查表方式：

> 📄 **原文**　書 p.28 ｜ PDF p.50
>
> Every plaintext letter tells the position of the row, and every keyword letter
> tells the position of the column.

書的示範：`t` 是第 20 個字母、`r` 是第 18 個，
所以查第 20 列第 18 行 → 得到 **K**。（我核對過，正確。）

#### 為什麼頻率分析失效了

書自己點出了關鍵：

> 📄 **原文**　書 p.28 ｜ PDF p.50
>
> the letter t is ­sometimes enciphered as a K and sometimes as a G since the
> relative key letter is once r and another time n.

**同一個明文字母 `t`，在不同位置變成不同的密文字母。**
明文的頻率分佈被打散了 —— 這正是 §2.2.4 書說要達成的目標。

### §2.4.2 💻 程式碼對照

書 §2.4.2 ｜ 書頁 29–33 ｜ PDF 51–55 ｜ [開啟](./cryptography-cpp.pdf#page=51)

**程式碼把整張 26×26 的 Vigenère 表寫死在原始碼裡**（書頁 29–31，佔了將近三頁）：

```cpp
charvigenere_table[26][26] = {
'A', 'B', 'C', 'D', ... 'Z',
'B', 'C', 'D', 'E', ... 'A',
...
};
```

加密函式是本章最短、也最漂亮的一段：

```cpp
void Encrypt (string in, string &out, string k) {
inti = 0;
for (string :: iterator it = in.begin(); it ! =
in.end(); it++) {
if (*it ! = ' ') {
int row = toupper(*it) - 'A';
int column = toupper(k[i% k.length()]) - 'A';
out + = vigenere_table[row][column];
     }
else {
out + = ' ';
     }
i++;
   }
}
```

| 程式碼 | 對應演算法 |
|---|---|
| `int row = toupper(*it) - 'A'` | 明文字母決定**列** |
| `k[i % k.length()]` | **Step 2** 金鑰用完從頭來 —— 又是 mod 在繞圈 |
| `int column = toupper(k[...]) - 'A'` | 金鑰字母決定**行** |
| `vigenere_table[row][column]` | 查表 |

解密則是反著找：固定行（金鑰字母），在那一行裡**由上往下掃**，
找到密文字母時的列號就是明文字母。

```cpp
for (row = 0; row < 26; row++) {
if (vigenere_table[row][column] = = *it) break;
         }
out + = 'A' + row;
```

> **注意這裡不需要 Vigenère 表也做得到。**
> 查表 `table[row][col]` 的值其實就是 `((row + col) % 26) + 'A'` ——
> 跟凱撒密碼是同一條算式，只是位移量每個字元都在變。
> 書選擇寫死一張表，讓「多張替換表輪流用」這個概念在程式碼裡看得見。

### §2.4.3 ⚠️ 這份實作的問題

#### 問題一：解密時直接丟掉你輸入的東西

`main` 的解密分支：

```cpp
else if (choice = = 2) {
input = output;
output.clear();
Decrypt(input, output, key);
```

程式**明明提示你輸入密文**（`"Enter cipertext..."`，並用 `getline` 讀進 `input`），
然後**第一行就把 `input` 覆寫成上一次加密的結果 `output`**。

**你打的東西被完全忽略。** 這支程式實際上只能解密它自己剛剛加密的內容 ——
一開機就選解密的話，`output` 是空字串，什麼都不會發生。

#### 問題二：空白會消耗金鑰

`i++` 寫在 `if/else` 之外，所以**空格也會讓金鑰前進一位**。
輸入 `to be` 和 `tobe` 會得到不同的密文。

不算錯誤（只要加解密一致就能還原），但這是實作決定，不是演算法的一部分。
**傳統的 Vigenère 通常先把空白剝掉。**

#### 問題三：解密只吃大寫

表裡存的是大寫字母，解密時比對 `vigenere_table[row][column] == *it` **沒有做 `toupper`**。
但輸入驗證同時允許大小寫。餵小寫密文進去，內層迴圈找不到匹配，
`row` 會停在 26，`out += 'A' + 26` 產生 `'['`。

### §2.4.4 為什麼會被破

書 §2.4.3 ｜ 書頁 33–34 ｜ PDF 55–56 ｜ [開啟](./cryptography-cpp.pdf#page=55)

**因為金鑰會重複。**

> 📄 **原文**　書 p.33 ｜ PDF p.55
>
> Even though polyalphabetic is more secure than simple substitution cipher, it can
> still be broken by analyzing the period.

書直接用表 2.4 的密文示範：

- 密文裡 `KIOV` 這個片段**隔了 9 個字母後重複出現**
- `NU` 這個片段**隔了 6 個字母後重複出現**
- 9 和 6 的公因數是 **3**
- 所以**金鑰長度很可能是 3** —— 而金鑰 `run` 確實是 3 個字母

> ⚠️ **書上把它印成 `KOIV`，這是筆誤**，密文裡的片段是 `KIOV`
> （見表 2.4：K I O V I E E I G **K I O V** N U…）。距離 9 是對的。

#### 為什麼公因數能洩漏金鑰長度

⚠️ **本段不是書上的內容。**

當**同一段明文**剛好對上**同一段金鑰**時，就會產生**同一段密文**。
而金鑰每隔「金鑰長度」個字元就重複一次 ——
所以兩次重複出現之間的距離，**必然是金鑰長度的倍數**。

蒐集多組重複片段的距離，取它們的**最大公因數**，就得到金鑰長度。

> 這個方法叫 **Kasiski examination（卡西斯基試驗）**，
> 1863 年由 Friedrich Kasiski 發表。**書沒有給這個名字**，但描述的就是它。

#### 破解的最後一步

書講完了怎麼找週期，然後說：

> 📄 **原文**　書 p.34 ｜ PDF p.56
>
> Frequency analysis is applicable here again by knowing which letters were encoded
> with the same key.

**一旦知道金鑰長度是 3，就把密文拆成 3 組**：
第 1、4、7、10… 個字元一組，第 2、5、8… 一組，第 3、6、9… 一組。

**每一組內部都是用同一個金鑰字母加密的 —— 也就是一個單純的凱撒密碼。**
對每一組各做一次頻率分析（或直接暴力試 25 種位移）就破了。

> **這就是整章的收尾**：多字母密碼把頻率打散了，
> 但只要找出週期，它就退化成「幾個獨立的凱撒密碼」，
> 而凱撒密碼在 §2.1.4 就已經破了。

## §2.5 把四個古典密碼放在一起看

這章的四節不是四個並列的例子，是**一條明確的軍備競賽路線**。
每一步都在回應「上一步是怎麼被破的」：

| 密碼 | 相對前一個做了什麼 | 金鑰空間 | 怎麼被破 |
|---|---|---|---|
| **Caesar** | — | **25** | 暴力破解（25 次） |
| **Monoalphabetic** | 位移 → **任意替換表** | **26! ≈ 4×10²⁶** | 頻率分析（金鑰空間再大也沒用） |
| **Playfair** | 單字母 → **雙字母一組** | 25 個字母的排列 | 雙字母頻率分析 ＋ 已知明文 |
| **Polyalphabetic** | 一張表 → **多張表輪流** | 26^(金鑰長度) | 找週期 → 退化成多個凱撒 |

### 三個一路帶到現代密碼學的教訓

**1. 金鑰空間大 ≠ 安全。**
Monoalphabetic 有 4×10²⁶ 把金鑰，被 26 個字母的統計打敗。
**安全性的瓶頸在最弱的攻擊面，不在最強的那個。**

**2. 統計結構會洩漏一切。**
四個密碼全部死於同一件事：**密文裡殘留了明文的統計特性。**
Caesar 保留單字母頻率、Playfair 保留雙字母頻率、Vigenère 保留週期性重複。

⚠️ **這正是現代區塊密碼的設計目標。** 你會在第 4～6 章看到
Shannon 提出的 **confusion（混淆）** 與 **diffusion（擴散）** ——
就是為了徹底摧毀這些統計結構。
（**書在這章沒有提到這兩個名詞**，但這章示範的就是「沒做到它們會怎樣」。）

**3. 重複使用金鑰是致命的。**
Vigenère 之所以被破，唯一的原因是**金鑰比訊息短，所以必須重複**。

⚠️ **本段不是書上的內容。** 如果金鑰**跟訊息一樣長、完全隨機、且只用一次**，
Vigenère 就變成 **one-time pad（一次性密碼本）**——
那是**唯一被數學證明無法破解**的密碼。
**書全書沒有提到 one-time pad**，這是第 2 章一個明顯的遺漏，
因為它正好是這章邏輯的終點。

### 這條線接到哪裡

- **Playfair 的「一次處理一組」** → 第 4 章 **Block Cipher**
- **Vigenère 的「金鑰流輪流用」** → 第 1 章提過的 **Stream Cipher**
- **「多輪處理、每輪換一張表」** → 第 3 章的**轉輪機**，再到第 5、6 章的 DES / AES

## ⚠️ 第 2 章的問題總表

| 位置 | 問題 | 嚴重度 |
|---|---|---|
| §2.1.1 Step 0 | 演算法說 A=1，程式碼是 A=0；用 A=1 會在 Z 上壞掉 | 中 |
| §2.1.2 `main` | 金鑰驗證放行 26（等於不加密），與 Step 1 矛盾 | 低 |
| §2.1.2 | 用大小寫決定加解密，這不是演算法的一部分 | **觀念混淆** |
| §2.1.1 Step 3 | 沒提 C++ 負數取餘的問題（程式碼有處理，描述沒說） | 低 |
| §2.2 文字 | 「26 keys」措辭錯誤，應為「一把金鑰＝一個排列，空間 26!」 | 中 |
| §2.2.2 | **產生的是凱撒位移表，不是隨機替換表**；去重檢查型別不符；`exist`/`num` 未初始化 | **嚴重** |
| §2.3.2 | Step 4（奇數補 x）未實作，改成把最後一個字母以明文留下；並有陣列越界 | **嚴重** |
| §2.3.2 | 解密刪除**所有** X（含明文原有的）；`erase` 後索引跳過 | 高 |
| §2.3.2 | 插入 x 後索引錯位，後續重複字母偵測失效 | 高 |
| §2.4.2 `main` | 解密分支丟棄使用者輸入，只能解自己剛加密的東西 | 高 |
| §2.4.2 | 解密未做 `toupper`，小寫密文產生 `'['` | 中 |
| §2.4.3 | 密文片段誤植為 `KOIV`，實際是 `KIOV` | 低（筆誤） |

### 這章沒有的東西

| 缺什麼 | 為什麼要緊 |
|---|---|
| **One-time pad** | 這章邏輯的自然終點，也是唯一可證明安全的密碼。全書 0 次 |
| **Kerckhoffs 原則** | 判斷這四個密碼「不安全」的判準，沒有被命名 |
| **Kasiski examination** | §2.4.3 描述了這個方法但沒給名字 |
| **Known-plaintext attack** | §2.3.3 描述了但沒給名字，第 3 章還會再用到 |
| **Confusion / Diffusion** | 現代密碼的設計目標，這章正好示範了「沒做到會怎樣」 |
| **CSPRNG** | §2.2.2 的災難根源。書用 `rand()`，且從未討論亂數品質 |

## 📌 第 2 章的三句話重點

1. **四個古典密碼死於同一件事** —— 密文保留了明文的統計結構。
   Caesar 保留單字母頻率、Playfair 保留雙字母頻率、Vigenère 保留週期。
2. **金鑰空間大不等於安全** —— Monoalphabetic 有 4×10²⁶ 把金鑰，
   卻被 26 個字母的頻率統計打敗。攻擊者不會照你設計的方式攻擊。
3. **書的程式碼跟書的文字經常對不起來** ——
   最嚴重的是 §2.2 那份號稱「隨機替換表」的實作，
   實際產生的是一張凱撒位移表，金鑰空間只有 26。

## 📖 第 2 章名詞小抄

| 英文 | 中文 | 一句話 |
|---|---|---|
| Substitution cipher | 替換式密碼 | 把每個字母換成另一個字母 |
| Caesar / Shift cipher | 凱撒／位移密碼 | 每個字母固定往後移 k 格，金鑰空間 25 |
| Monoalphabetic cipher | 單字母替換密碼 | 一張任意的一對一替換表，金鑰空間 26! |
| Polyalphabetic cipher | 多字母替換密碼 | 多張替換表輪流用 |
| Vigenère cipher | 維吉尼亞密碼 | 多字母密碼的代表，金鑰是一個單字 |
| Tabula recta / Vigenère table | 維吉尼亞方陣 | 26×26 的查表，每列是一個位移不同的凱撒 |
| Playfair cipher | 普萊費爾密碼 | 5×5 矩陣，一次加密一對字母 |
| Digraph | 雙字母組 | 相鄰的兩個字母，Playfair 的處理單位 |
| Brute-force attack | 暴力破解 | 把所有金鑰試一遍 |
| Frequency analysis | 頻率分析 | 用字母出現頻率的統計反推替換關係 |
| Period | 週期 | 多字母密碼中金鑰重複的間隔 |
| Key space | 金鑰空間 | 所有可能金鑰的數量 |
| Kasiski examination | 卡西斯基試驗 | 用重複片段的距離公因數推出金鑰長度（⚠️ 書未命名） |
| Known-plaintext attack | 已知明文攻擊 | 靠猜中部分明文來反推金鑰（⚠️ 書未命名） |
| One-time pad | 一次性密碼本 | 金鑰與訊息等長、隨機、只用一次（⚠️ 全書未提） |

---
---

# 第 3 章 轉輪機

**Rotor Machine** ｜ 作者 Sheikh Shaugat Abdullah、Saiful Azad
書頁 35–44 ｜ PDF 57–66 ｜ [開啟](./cryptography-cpp.pdf#page=57)

> 古典密碼的終點站。用機械把多字母替換推到人手算不出來的規模 ——
> 也是「密碼學從人工進入機器」的分界。

## §3.0 這章在解什麼問題

第 2 章的結論是：**Vigenère 敗在金鑰太短、必須重複。**
那把金鑰加長不就好了？

問題在於 —— **人手算不出來。** 一個 20 個字母的金鑰，
你要在紙上對 20 張不同的替換表，一個字母一個字母查，錯一個就全毀。

轉輪機的答案是：**讓機器來轉。**

書給的歷史背景：第一台機械加密裝置在 **1920 年**問世，名為 rotor machine。
最有名的例子是德國人發明的 **Enigma**，二戰期間大量使用。

書特別花篇幅講了發明權的爭議：曾有四個人被認為是發明者
（Edward Hebern、Arvid Damm、Hugo Koch、Arthur Scherbius），
但後來發現最早的發明者是**兩位荷蘭海軍軍官** ——
Theo A. van Hengel 與 R.P.C. Spengler，**1915 年**。
這是本章唯一附了正式參考文獻的地方（de Leeuw, *Cryptologia*, 2003）。

## §3.1 為什麼需要轉輪機

書 §3.1 ｜ 書頁 36 ｜ PDF 58 ｜ [開啟](./cryptography-cpp.pdf#page=58)

書直接承接第 2 章，把整條線重講了一遍：

> 📄 **原文**　書 p.36 ｜ PDF p.58
>
> monoalphabetic ciphers replace one character/letter with another character. This
> technique is vulnerable, since a simple frequency analysis could find out the
> plaintext easily. Therefore, polyalphabetic ciphers are ­proposed [...] However,
> since ciphertext is calculated by hand, only a handful of different alphabets can
> be utilized.

**關鍵句是最後一句**：因為密文是**用手算的**，所以只能用少少幾張替換表。

> 📄 **原文**　書 p.36 ｜ PDF p.58
>
> The invention of rotor machines resolved that limitation, which provides a
> realistic way of using a huge number of alphabets.

**這是一個工程上的突破，不是數學上的。** 演算法的想法（多表替換）第 2 章就有了，
轉輪機做的是**讓它在實務上可行**。

> ⚠️ **這個模式在密碼學史上一再重演。** RSA 的數學在 1970 年代就有了，
> 但要等到電腦夠快才實用；橢圓曲線同理。
> **「想得到」和「做得到」之間永遠隔著一層工程。**

## §3.2 基本結構：鍵盤 ＋ 一串轉子

書 §3.2 ｜ 書頁 36–37 ｜ PDF 58–59

**一台轉輪機 = 一個鍵盤 + 一串轉子（rotor）。**

- **一個轉子就是一張接線好的替換表** ——
  書的說法是 "a mechanical wheel wired to perform a general substitution"。
- 轉子**串接**：前一個轉子的輸出接腳，接到下一個轉子的輸入。

書上圖 3.1 畫了一台**三轉子、八字母**的簡化機器，
分別畫出第一個轉子**轉動一格前**和**轉動一格後**的接線狀態。

### 訊號怎麼跑

書的例子很清楚：

> 📄 **原文**　書 p.37 ｜ PDF p.59 ｜ [開啟](./cryptography-cpp.pdf#page=59)
>
> in a three-rotor machine, the first rotor might ­substitute A » E, the second rotor
> might substitute E » K, and the third rotor might substitute K » Y. Therefore,
> after encryption, A will become Y.

**A → E → K → Y。** 一個字母連續穿過三張替換表。

### 轉動：這才是重點

> 📄 **原文**　書 p.37 ｜ PDF p.59
>
> To protect data frequency analysis, some of the rotors shift after each output.

**每輸出一個字母，就有轉子轉動一格 —— 於是替換表變了。**

這就是它跟 Vigenère 的差別：Vigenère 有 L 張表輪流用（L = 金鑰長度），
轉輪機的表**每按一次鍵就換一張**，而且要按很久才會轉回原點。

### 組合數有多大

書寫的是：

> 📄 **原文**　書 p.37 ｜ PDF p.59
>
> a combination of sev­eral rotors and shifting of n number of rotors leads to a 26n.

⚠️ **書上這裡印成 `26n`，正確應該是 `26ⁿ`**（26 的 n 次方）——
排版把上標弄丟了。從上下文可以確認：n 個轉子，每個有 26 個位置，
組合數是 26 × 26 × … × 26 = **26ⁿ**。

三個轉子就是 26³ = **17,576** 種狀態。
換句話說：**金鑰流的週期是 17,576**，遠遠超過任何人手抄的 Vigenère 金鑰。

> **對照第 2 章**：Vigenère 用金鑰 `run` 的週期是 3，九個字母就露出重複片段。
> 三轉子機要一萬七千多個字母才重複一次。
> **這就是「機械化」帶來的量變。**

## §3.3 系統化：把機械動作寫成可計算的規則

書 §3.3 ｜ 書頁 37 ｜ PDF 59

書在這一節說明**為什麼多字母替換難以機械化**：

> 📄 **原文**　書 p.37 ｜ PDF p.59
>
> It is relatively straightforward to create a machine to perform simple substitution
> in monoalphabetic algorithms. However, it is challeng­ing to create a machine that
> can perform polyalphabetic substitutions.

單表替換只要一組固定接線就行；多表替換要**接線會變**。

書給的解法一句話講完：

> 📄 **原文**　書 p.37 ｜ PDF p.59
>
> the idea is to change the wiring of the machine with each keystroke. The wiring is
> placed inside a rotor. After a keystroke, the rotor is rotated with a gear.
> Therefore, a key­stroke that outputs an S might generate an A the next time.

**把接線裝在一個會轉的輪子裡，按一次鍵齒輪就把它推一格。**

書強調的結果是：**「同一個按鍵，這次輸出 S，下次可能輸出 A。」**

> ⚠️ **這句話值得停下來想一下。** 這正是第 2 章 §2.2.4 說的
> 「打散頻率分佈」的極致版本 —— 不只是幾張表輪流，而是**幾乎每次都不同**。

## §3.4 演算法

書 §3.4 ｜ 書頁 37 ｜ PDF 59

書給了三個步驟：

> 📄 **原文**　書 p.37 ｜ PDF p.59
>
> Step 0: Select how many rotors will be used and make the rotors ready by placing 26
> unique random character pairs.
> Step 1: To encrypt, for each character in the alphabet set, for each rotor, find the
> match from the rotor pair sequentially. After each encryption, rotate the rotors
> accordingly.
> Step 2: To decrypt, apply the same procedure of step 1, with reverse sequential
> order of the rotors.

三個重點：

1. **一個轉子 = 26 組「不重複的」字元配對。**
   「不重複」（unique）這個字很關鍵 —— 它保證這張表是**一對一的排列**，
   也就是可逆的。（對照第 2 章 §2.2.3 的災難：那份程式碼沒做到這件事。）
2. **加密時依序穿過每個轉子**，每加密一個字元後轉動轉子。
3. **解密就是反過來，以相反的順序穿過轉子。**

⚠️ **Step 0 有一個沒說清楚的地方**：「選擇要用幾個轉子」——
但書上的實作**寫死成三個**，沒有做成可調參數。

## §3.5 💻 程式碼對照

書 §3.5 ｜ 書頁 37–43 ｜ PDF 59–65 ｜ [開啟](./cryptography-cpp.pdf#page=59)

這是本章的主體（7 頁），寫成一個 `class Enigma`。

### 資料結構：轉子是一串「配對」

```cpp
typedef pair<int,int>Rotor_Pair;
...
vector<Rotor_Pair>first_rotor;
vector<Rotor_Pair>second_rotor;
vector<Rotor_Pair>third_rotor;
vector< vector <Rotor_Pair>>all_rotors;
int count;
```

**一個轉子 = 26 個 `pair<int,int>`**，每個 pair 是「輸入接腳 → 輸出接腳」的對應。
`all_rotors` 保存三個轉子的**原始狀態**（解密前要還原用）。
`count` 記錄已經處理了幾個字元，決定何時該轉動第二、第三個轉子。

### 建轉子：`create_rotor()`

**照書原樣轉錄**：

```cpp
void Enigma::create_rotor(vector <Rotor_Pair>&rtq)
{
vector<int>temp_q;
int current = rand()% 26 + 1;
intnum = rand()% 26 + 1;
rtq.push_back(make_pair(current,num));
temp_q.push_back(num);
for (inti = 0; i< 25; i++) {
current = current% 26 + 1;
bool exist = true;
    //Selecting unique random pairs for each of the
rotors
while (exist) {
exist = false;
num = rand()% 26 + 1;
for(vector <int> :: iterator it = temp_q.begin(); it
   ! = temp_q.end(); it++) {
if ((*it) = = num) {
exist = true;
break;
           }
        }
    }
temp_q.push_back(num);
Rotor_Pairrp = make_pair(current,num);
rtq.push_back(rp);
   }
}
```

對回 **Step 0**：產生 26 組不重複的配對。

- `current = current % 26 + 1` —— 輸入接腳從一個隨機起點開始，**循環走完 1～26**。
- `num = rand() % 26 + 1` —— 輸出接腳隨機取，
  用 `temp_q` 記錄用過的值，重複就重抽。

### ⚠️ 對照第 2 章：同樣的去重，這次寫對了

**這段跟第 2 章 §2.2.2 的去重邏輯長得幾乎一模一樣，但這一份是正確的**，
差別有兩處：

| | 第 2 章 `PutCharInVec()` | 第 3 章 `create_rotor()` |
|---|---|---|
| `exist` 初始化 | `bool exist;` **未初始化** | `bool exist = true;` ✅ |
| 比對的型別 | `vector<char>` 存 65–90，比對 `num`（1–26）→ **永遠不相等** | `vector<int>` 存 1–26，比對 `num`（1–26）→ ✅ |
| 實際產出 | **一張凱撒位移表** | **一個真正的隨機排列** ✅ |

**同樣兩位作者，第 3 章寫對了，第 2 章沒有。**
高度懷疑第 2 章那份是這份的錯誤改寫版。

> 這也再次說明為什麼要**把兩章的程式碼對著讀** ——
> 單看第 2 章你不會知道作者其實懂怎麼寫；對照之後才確定那是 bug 而非設計。

### ⚠️ 但這台機器根本沒有金鑰

`manage_rotors()` 裡有一行：

```cpp
void Enigma :: manage_rotors ()
{
count = 0;
srand (5);
create_rotor(first_rotor); //Creating the first rotor
...
```

**`srand(5)` 是固定的亂數種子。**

`rand()` 是**虛擬**亂數 —— 給同一個種子，它會產生**完全相同的數列**。
所以這支程式**每次執行產生的三個轉子接線完全一樣**。

**結論：這台機器沒有金鑰。** 任何人拿到這份原始碼，
就能重建出一模一樣的機器，直接解密所有訊息。

而且 `main()` 還會呼叫 `display_rotors()` **把轉子接線印在螢幕上**。

> ⚠️ 這正是第 1 章 §1.5 提過的坑 —— **cryptosystem 的定義少了 KeyGen**，
> 而現實中最常見的崩潰就發生在金鑰產生這一步。**書在這裡自己踩了一次。**
>
> 真正的 Enigma 的金鑰是什麼？是**轉子的選擇與順序、轉子的起始位置、
> 以及插線板（plugboard）的接法** —— 這些每天更換，寫在密碼本上。
> **書上的實作把這些全部省略了。**（⚠️ plugboard 全書未提。）

### 加密一個字元：`transpos_en()`

**照書原樣轉錄關鍵片段**：

```cpp
char Enigma :: transpos_en (char ch)
{
count++;
ch = toupper (ch);
intpos = ch - 65 + 1; //Converting ASCII to decimal
int index = 0;
  // Finding the specific position for each of the character
for (vector <Rotor_Pair> :: iterator it = first_rotor.
begin(); it ! = first_rotor.end(); it++) {
if ((*it).second = = pos) break;
else index++;
   }
  // Rotating the first rotor
Rotor_Pairtrp = first_rotor.front();
first_rotor.erase(first_rotor.begin());
first_rotor.push_back(trp);
pos = (second_rotor[index]).first;
...
  // Rotating the second rotor
if (count% 26 = = 0) { ... }
...
  // Rotating the third rotor
if (count% 676 = = 0) { ... }
ch = pos - 1 + 65; //Converting Decimal to ASCII
returntolower(ch);
}
```

#### 對回演算法

| 程式碼 | 對應 |
|---|---|
| `pos = ch - 65 + 1` | 字母 → 數字（A = 1，注意這裡是 **A=1** 不是 A=0） |
| 三段 `for` 迴圈找 `.second == pos` | **Step 1** 「依序穿過每個轉子」 |
| `erase(begin())` + `push_back(trp)` | **轉子轉動一格** —— 把第一個元素搬到最後面 |
| `count % 26 == 0` | 第二個轉子每 **26** 個字元轉一次 |
| `count % 676 == 0` | 第三個轉子每 **676**（= 26²）個字元轉一次 |

#### 里程表式的進位

`26` 和 `676` 這兩個數字是這份實作最漂亮的地方。

**第一個轉子每按一次鍵轉一格；它轉滿一圈（26 格）之後，第二個轉子才轉一格；
第二個轉子轉滿一圈（再 26 次，共 676 次按鍵）之後，第三個轉子才轉一格。**

**這就是汽車里程表的進位方式** —— 個位跑滿十格，十位才進一格。
真正的 Enigma 就是這樣運作的（機械上靠一個叫 notch 的凹口帶動）。

> 這也解釋了 §3.2 的 26ⁿ 從哪裡來：
> 三個轉子要 26 × 26 × 26 = 17,576 次按鍵才會全部回到起點。

### 解密：`transpos_de()`

結構跟加密對稱，但方向相反 ——

- **順序反過來**：第三個轉子 → 第二個 → 第一個（對應 **Step 2**）
- **查找方向反過來**：加密時找 `.second` 取 `.first`，解密時找 `.first` 取 `.second`

我把代數推過一遍，**這個反向查表的邏輯是正確的**，
在轉子位置一致的前提下 `transpos_de(transpos_en(x)) == x`。

## §3.6 ⚠️ 這份實作的三個問題

⚠️ **本節是我對書上程式碼的逐行推導，依 brief 規定本輪不編譯不執行。**

### 問題一：`decrypt()` 沒有重置計數器 —— 解密會失敗

`decrypt()` 開頭做了兩件事：從 `all_rotors` 還原三個轉子的初始狀態，然後開始解密。
但它是這樣寫的：

```cpp
void Enigma :: decrypt ()
{
   ...
   // initializing the rotor settings
int count = 0;
for (vector < vector <Rotor_Pair>> :: iterator p =
all_rotors.begin(); p ! = all_rotors.end(); p++) {
       if (count = = 0) first_rotor = *p;
       else if (count = = 1) second_rotor = *p;
       elsethird_rotor = *p;
       count++;
}
```

**那個 `int count = 0;` 是一個區域變數，它遮蔽（shadow）了同名的成員變數 `count`。**

它只被用來當這個 for 迴圈的計數器（0、1、2 決定放進哪個轉子），
**成員的 `count` 完全沒有被重置。**

後果：加密處理了 N 個字元後，成員 `count` 停在 N。
解密開始時 `count` 從 **N+1** 繼續往上數 ——
於是 `count % 26 == 0` 和 `count % 676 == 0` 的觸發時機，
**跟加密時落在完全不同的字元位置上**。

**第二、第三個轉子的進位時機錯開了，解密結果就是錯的。**

> 只有在訊息很短、而且加密區間 `1..N` 和解密區間 `N+1..2N`
> 都沒有跨過 26 的倍數時，才會碰巧解對 —— 也就是**短訊息可能看起來正常**，
> 長一點就壞掉。這種 bug 最難發現。

這違反了第 1 章 §1.5 提到的**正確性條件** `Decrypt(Encrypt(M)) = M`。

### 問題二：`transpos_en()` 第三段迴圈用錯了容器

```cpp
for (vector <Rotor_Pair> :: iterator it = third_rotor.
begin(); it ! = second_rotor.end(); it++) {
if ((*it).second = = pos) break;
   }
```

**迭代器從 `third_rotor` 開始，卻拿 `second_rotor.end()` 當終止條件。**

比較兩個屬於不同容器的迭代器在 C++ 裡是**未定義行為**。
實務上這個迴圈可能永遠不停、可能立刻停、可能讀到不屬於它的記憶體。

另外注意：前兩段迴圈都有 `else index++;`，**這一段沒有** ——
所以就算它跑完，`index` 也永遠是 0。

**不過**：這段迴圈的結果（`index`）在它之後**完全沒有被使用** ——
輸出用的 `pos` 在迴圈之前就已經算好了（`pos = (third_rotor[index]).first;`）。

**所以這整段是死碼（dead code）**，除了那個未定義行為之外不影響輸出。
`transpos_de()` 裡對應的那段也是死碼，但它至少沒有用錯容器。

> 這暗示這兩個函式是**互相複製貼上**改出來的，而且改的時候漏了一處。

### 問題三：標點符號會被吃掉

```cpp
if (isalpha(*it))
output + = transpos_en(*it);
else output + = 32;
```

**所有非字母字元一律變成 ASCII 32（空格）。**
逗號、句號、數字全部被抹成空格，而且**解密也還原不回來**。

不算安全問題（真正的 Enigma 也只處理 26 個字母），但這是資料損失，
書沒有說明這個限制。

## §3.7 為什麼還是被破了

書 §3.6 ｜ 書頁 43 ｜ PDF 65 ｜ [開啟](./cryptography-cpp.pdf#page=65)

書開宗明義：

> 📄 **原文**　書 p.43 ｜ PDF p.65
>
> The technique used in the rotor machine was very strong if used ­correctly and
> securely. However, the German messages encrypted with the rotor machine Enigma were
> deciphered by the Allies ­during World War II.

**「if used correctly and securely」（如果被正確且安全地使用）—— 全部的重點都在這一句。**

書說有人主張這次密碼分析讓**二戰縮短了兩年**。

### 書給的破解方式：弱訊息金鑰

書聚焦在波蘭數學家兼密碼學家 **Marian Rejewski** 身上：

> 📄 **原文**　書 p.43 ｜ PDF p.65
>
> What he assumed, and later on discovered to be true, was that most of the time the
> German operators would choose very simple message keys, like AAA or XYZ or ABC.

**Rejewski 猜（後來證實）德軍操作員大多會選 `AAA`、`XYZ`、`ABC` 這種偷懶的訊息金鑰。**

於是他把所有可能的簡單訊息金鑰列成清單，用它來找出真正的金鑰 ——
書說他因此能在很短時間內破解大量密文。

### ⚠️ 這正是第 1 章那句話的應驗

回頭看第 1 章 §1.10，書說整體安全取決於三件事，第三件是
**"how well people use the procedures, processes, and technology"**（人有多會用）。

> **Enigma 沒有被數學打敗，是被人的習慣打敗的。**
> 機器的組合數是 26ⁿ 級別，但操作員從中只實際使用了幾十種。
>
> **金鑰空間大不等於安全** —— 這跟第 2 章 §2.2.4 的教訓是同一條，
> 只是那次的兇手是語言的統計特性，這次是人的偷懶。

### ⚠️ 書漏掉的部分

⚠️ **本段不是書上的內容。** 書對 Enigma 破解的敘述**只有一段、只講了 Rejewski**。
以下是書完全沒有提到、但屬於這段歷史核心的東西：

| 書沒講的 | 為什麼重要 |
|---|---|
| **Reflector（反射器）的致命弱點** | 真正的 Enigma 有一個反射器，讓加密具有對合性（加密和解密是同一個操作）。代價是**任何字母都不會被加密成它自己**。這個看似無害的性質是後續攻擊的關鍵槓桿 |
| **Crib（已知明文）** | 破解實務上大量依賴猜中固定格式的明文片段（例如每日的天氣報告）。**這就是第 2 章 §2.3.4 出現過的 known-plaintext attack**，書兩次描述它都沒給名字 |
| **Bletchley Park、Alan Turing、bombe** | 波蘭的成果在戰前移交英國後，英方才規模化破解 |
| **Plugboard（插線板）** | 真正 Enigma 的金鑰主體之一。書上的實作和敘述都沒有它 |

> **提醒**：依 brief，缺口**只標記不補**。上表是為了讓你知道
> 「這章沒告訴你的事有哪些」，不是這份筆記要教的內容。
> 想深入的話這是一個獨立的題目。

## §3.8 從轉輪機到現代 block cipher

⚠️ **本節是我加的整理，不是書上的章節。**

轉輪機是古典密碼的終點，但它留下的兩個設計想法**直接變成現代密碼的骨架**：

### 想法一：多輪處理（multiple rounds）

一個字母連續穿過三個轉子 —— **每一層都做一次替換，層層疊加。**

> 這就是 **round（回合）** 的雛形。
> 第 5 章的 **DES 有 16 個回合**，第 6 章的 **AES 有 10～14 個回合**。
> 單一回合的變換很弱，但疊很多層之後就難以逆推。

### 想法二：每一步都改變狀態

按一次鍵，轉子就轉一格，替換表就變了 ——
**加密函式本身在過程中不斷改變。**

> 現代區塊密碼用 **key schedule（金鑰排程）** 達成同樣的效果：
> 從主金鑰推導出每個回合各自不同的 **round key**，每一輪用不同的金鑰。
> 你會在第 5 章 DES 和第 6 章 AES 各看到一次。

### 但有一個關鍵差異

⚠️ **轉輪機仍然是逐字元處理的**（一次一個字母，本質上是串流密碼）。

**第 4 章開始換成另一種思路：把資料切成固定大小的區塊，一次處理一整塊。**
那是 block cipher，也是接下來三章的主題。

## ⚠️ 第 3 章的問題總表

| 位置 | 問題 | 嚴重度 |
|---|---|---|
| §3.2 | `26n` 應為 `26ⁿ`，排版把上標弄丟 | 低（排版） |
| §3.4 Step 0 | 說「選擇要用幾個轉子」，但實作寫死三個 | 低 |
| §3.5 `manage_rotors` | **`srand(5)` 固定種子 → 這台機器沒有金鑰**，且會把接線印在螢幕上 | **嚴重** |
| §3.5 `decrypt` | 區域 `count` 遮蔽成員 `count`，計數器沒重置 → **解密結果錯誤** | **嚴重** |
| §3.5 `transpos_en` | 第三段迴圈拿 `second_rotor.end()` 當 `third_rotor` 的終止條件 → 未定義行為（且該段是死碼） | 高 |
| §3.5 `encrypt` | 非字母一律變成空格，資料損失且不可還原 | 中 |
| §3.6 | 破解敘述只有 Rejewski 一段，漏掉反射器弱點、crib、Bletchley Park、plugboard | 中（內容深度） |

### 這章沒有的東西

| 缺什麼 | 為什麼要緊 |
|---|---|
| **Plugboard** | 真正 Enigma 金鑰的主要組成之一 |
| **Reflector 與它的弱點** | 破解 Enigma 的關鍵槓桿 |
| **Known-plaintext attack / crib** | 第 2、3 章各描述了一次，兩次都沒命名 |
| **CSPRNG** | `srand(5)` 這個坑的根源，全書無專章 |

## 📌 第 3 章的三句話重點

1. **轉輪機是工程突破，不是數學突破** ——
   多表替換的想法第 2 章就有了，轉輪機讓它在實務上可行（26ⁿ 的週期）。
2. **Enigma 沒有被數學打敗，是被人的習慣打敗的** ——
   操作員愛用 `AAA`、`ABC` 這種訊息金鑰，把巨大的金鑰空間縮成幾十種。
3. **轉輪機留下的兩個想法直接變成現代密碼的骨架** ——
   **多輪處理**（→ DES 的 16 回合、AES 的 10–14 回合）
   與**每步改變狀態**（→ key schedule 的 round key）。

## 📖 第 3 章名詞小抄

| 英文 | 中文 | 一句話 |
|---|---|---|
| Rotor machine | 轉輪機 | 用機械轉子實現多表替換的加密裝置，1920 年問世 |
| Rotor | 轉子 | 一個接線好的輪子，等於一張替換表 |
| Enigma | 恩尼格瑪 | 最有名的轉輪機，德軍二戰使用 |
| Keystroke | 按鍵 | 每按一次鍵，轉子轉一格，替換表就變了 |
| Round | 回合 | 一次完整的變換；轉輪機的「穿過一個轉子」是它的雛形 |
| Key schedule | 金鑰排程 | 從主金鑰推導出每回合各自的 round key（⚠️ 本章未提，第 5 章開始出現） |
| Plugboard | 插線板 | 真正 Enigma 的金鑰組成之一（⚠️ 全書未提） |
| Reflector | 反射器 | 讓 Enigma 加解密對稱，但導致「字母不會變成自己」的弱點（⚠️ 全書未提） |
| Message key | 訊息金鑰 | 每則訊息各自的轉子起始位置；德軍愛用 AAA、ABC，因此被破 |
| `srand()` / seed | 亂數種子 | 固定種子 → 每次產生相同的「亂數」→ 等於沒有金鑰 |

---
---

# 第 4 章 區塊密碼

**Block Cipher** ｜ 作者 Tanveer Ahmed、Mohammad Abul Kashem、Saiful Azad
書頁 45–56 ｜ PDF 67–78 ｜ [開啟](./cryptography-cpp.pdf#page=67)

> ⚠️ **這是全書第一個完全沒有程式碼的章節。** 12 頁全是理論與示意圖，
> 所以本章沒有 `💻 程式碼對照`。
>
> 這章也是**第 1～3 章與第 5、6 章之間的橋** ——
> 它不介紹任何一個具體的密碼，而是講「現代區塊密碼**長什麼形狀**」，
> 讀完才有辦法看懂 DES 和 AES。

## §4.0 這章在解什麼問題

三個問題，對應這章的三個部分：

1. **一個好的密碼演算法應該具備什麼性質？** → Shannon 的 confusion 與 diffusion
2. **要怎麼組裝才能得到那些性質？** → Feistel 結構
3. **訊息比一個區塊長怎麼辦？** → 五種 mode of operation

> **第三個問題是這章最實用的部分。** 第 5、6 章教你 DES 和 AES 怎麼加密
> **一個 64 或 128 bit 的區塊** —— 但你的檔案有幾 MB。
> 中間差的那一段，就是這章的 §4.3。

## §4.1 從逐字元到逐區塊

書一開頭就把兩種形態並排定義：

> 📄 **原文**　書 p.45 ｜ PDF p.67 ｜ [開啟](./cryptography-cpp.pdf#page=67)
>
> A stream cipher is one that encrypts/decrypts a data stream character by
> character, i.e., one character at a time. [...] a block cipher encrypts/decrypts a
> block of n characters and produces an output of similar length.

**注意 "produces an output of similar length"** —— 區塊密碼的輸出長度等於輸入長度。
n bit 進去，n bit 出來。這個性質在後面談 padding 時會變成問題。

書點名 **DES** 和 **AES** 是區塊密碼的例子（第 5、6 章的主角），
並說目前多數對稱式區塊密碼都建立在 **Feistel 結構**之上。

### ⚠️ 書上這裡有兩個問題

**問題一：章號指錯了。**

> 📄 **原文**　書 p.45 ｜ PDF p.67
>
> All the ciphers discussed in Chapter 3 are stream ciphers.

第 3 章只有**一個**密碼（轉輪機）。作者想講的應該是**第 2 章和第 3 章**——
凱撒、單字母替換、Playfair、多字母替換、轉輪機，這些全都是逐字元處理。

（Playfair 嚴格說是一次兩個字元，算是一種很小的區塊，但書把它歸在這裡不算離譜。）

**問題二：這句話沒有根據。**

> 📄 **原文**　書 p.46 ｜ PDF p.68
>
> In general, block cipher algorithms ensure higher security over stream cipher
> algorithms.

⚠️ **兩種形態都可以是安全的，也都可以是不安全的。** 安全性取決於具體的演算法設計，
不取決於它是逐位元還是逐區塊。ChaCha20（串流）和 AES（區塊）在今天都被認為是安全的。

> 這跟第 1 章 §1.3 那句「串流密碼現代不太用了」是**同一個偏見的兩次出現**。
> 這本書對串流密碼有系統性的低估。

## §4.2 Shannon 的兩個原則：confusion 與 diffusion

書 §4.1 ｜ 書頁 46 ｜ PDF 68 ｜ [開啟](./cryptography-cpp.pdf#page=68)

**這一節是整章觀念上的核心，也直接回答了第 2 章留下的問題。**

書說 Shannon 提出兩個原則，任何安全的密碼系統都應該遵循。

### 先補一個工具：XOR（互斥或）

⚠️ **本段不是書上的內容。** 但從這章開始，**XOR 會出現在每一條公式裡**，
書卻從來沒有解釋過它，所以在這裡補。

XOR 寫作 `⊕`，是一個**逐位元**的運算，規則只有一條：**相同得 0，不同得 1。**

| a | b | a ⊕ b |
|---|---|---|
| 0 | 0 | **0** |
| 0 | 1 | **1** |
| 1 | 0 | **1** |
| 1 | 1 | **0** |

它有三個性質，**整章的公式都靠這三條**：

```
a ⊕ a = 0        任何東西跟自己 XOR 得到 0
a ⊕ 0 = a        跟 0 XOR 不變
(a ⊕ b) ⊕ b = a  ← 關鍵：XOR 兩次就回到原點
```

**第三條是為什麼 XOR 能拿來加密。** 把明文跟金鑰 XOR 得到密文，
密文再跟同一把金鑰 XOR 就變回明文 —— **加密和解密是同一個動作。**

> 這也解釋了 §4.7 和 §4.8 會出現的怪事：
> CFB 和 OFB 模式**解密時用的是加密函式**，不是解密函式。

### Confusion（混淆）

書的定義：

> 📄 **原文**　書 p.46 ｜ PDF p.68
>
> Shannon said confusion makes the relation between the key and the ciphertext as
> complex as possible.

**Confusion 管的是「金鑰 ↔ 密文」的關係，要讓它盡可能複雜。**

書給的判準：**密文的每個字元都應該取決於金鑰的好幾個部分**，
而且這個依賴關係在攻擊者看來必須像是隨機的。
書說達成的手段是「複雜的替換（substitution）技術」。

#### ⚠️ 書中間插了一句自相矛盾的話

> 📄 **原文**　書 p.46 ｜ PDF p.68
>
> This relationship needs to be loosened in such a way that even though the attacker
> gets some grip on the statistics of the ciphertext, he or she may not be able to
> deduce the key.

**"loosened"（放鬆／鬆開）跟前一句的 "as complex as possible"（盡可能複雜）矛盾。**

要的是**複雜化**，不是**鬆開**。作者想表達的大概是
「讓攻擊者無法從密文的統計特性反推金鑰」——
**這個目標是對的，但 "loosened" 這個動詞用錯了。**

**記前一句就好**：confusion = 金鑰與密文的關係盡可能複雜。

### Diffusion（擴散）

書的定義：

> 📄 **原文**　書 p.46 ｜ PDF p.68
>
> This refers to the property that the statistical ­structure of the plaintext is
> dissipated into long-range sta­tistics of the ciphertext.

**Diffusion 管的是「明文 ↔ 密文」的關係，要讓明文的統計結構被打散。**

書說得很明白：**擴散把單一個明文字元的影響散佈到很多個密文字元上。**
達成的手段是「排列（permutation）＋函式」反覆施加。

#### ⚠️ 書的定義句末尾有筆誤

> 📄 **原文**　書 p.46 ｜ PDF p.68
>
> diffusion spreads the influence of a single plaintext character over many
> ciphertext characters, or in other words, each ciphertext character is affected by
> many ciphertext characters.

**最後那個 "ciphertext characters" 應該是 "plaintext characters"。**

照字面讀，「每個密文字元被很多個密文字元影響」是**循環的、沒有意義的**。
前半句已經把正確的意思講對了：一個明文字元影響很多密文字元；
反過來說就是**一個密文字元被很多明文字元影響**。

#### ⚠️ 順帶：Shannon 的名字拼錯了

書上寫 **"Calude Shannon"**，正確是 **Claude Shannon**。
（有趣的是章末的參考文獻 [2] 寫的是正確的 "C. Shannon"，
所以只有內文拼錯。）

### 為什麼這兩個原則正好回答了第 2 章

⚠️ **本段不是書上的內容，但這是這章跟前面連起來的關鍵。**

回頭看第 2 章 §2.5 的結論：**四個古典密碼全部死於「密文保留了明文的統計結構」。**

**那正是 diffusion 不足。**

| 古典密碼 | 殘留了什麼統計結構 | 缺哪個原則 |
|---|---|---|
| Caesar | 單字母頻率完整保留 | Diffusion（一個明文字元只影響一個密文字元） |
| Monoalphabetic | 單字母頻率完整保留 | Diffusion |
| Playfair | 雙字母頻率保留 | Diffusion（影響範圍只有 2 個字元） |
| Vigenère | 週期性重複 | Confusion（金鑰與密文的關係太簡單：就是加法） |

**Shannon 在 1949 年把第 2 章的教訓寫成了設計原則。**
這章接下來的 Feistel 結構，就是實現這兩個原則的一種具體做法。

## §4.3 Feistel 結構

書 §4.2 ｜ 書頁 46–48 ｜ PDF 68–70 ｜ [開啟](./cryptography-cpp.pdf#page=68)

書上圖 4.1 畫了完整的 Feistel 網路（左邊加密、右邊解密，各 16 輪）。

### 運作方式

1. **把 n bit 的明文區塊切成兩半**：左半 `LE₀`、右半 `RE₀`，各 n/2 bit。
2. **讓這兩半通過 r 輪**（圖上畫 16 輪）。
3. **每一輪用一把不同的子金鑰 `Kᵢ`**，由主金鑰 K 推導而來。
   書強調所有子金鑰彼此不同、也跟 K 不同。
4. 每一輪做的事：

```
LEᵢ = REᵢ₋₁
REᵢ = LEᵢ₋₁ ⊕ F(REᵢ₋₁, Kᵢ)
```

白話：**右半原封不動搬到左邊；左半跟「右半經過輪函式 F 加工後的結果」XOR，
放到右邊。**

5. 最後一輪結束後把兩半合起來，就是密文。

書指出每一輪同時包含**替換**（左半 XOR 上 F 的輸出）與**排列**（兩半交換）——
正好對應 §4.2 的 confusion 與 diffusion 兩個手段。

### ⚠️ 書在這裡用錯了 XOR 的符號

書上印的是：

```
REᵢ = LEᵢ₋₁ ⊗ F(REᵢ₋₁, Kᵢ)
```

**那個 `⊗`（圈叉）不是 XOR，XOR 是 `⊕`（圈加）。**

怎麼確定是筆誤？**因為書自己在下一節就用對了** ——
§4.3.2 的 CBC 公式寫的是 `Cᵢ = E_K(Pᵢ ⊕ Cᵢ₋₁)`，用的是正確的 `⊕`。

**同一章裡兩種符號指同一個運算。** 讀的時候把 §4.2 的 `⊗` 一律當成 `⊕`。

### 解密

書給的解密公式：

```
REᵢ₋₁ = LEᵢ
LEᵢ₋₁ = REᵢ ⊕ F(REᵢ₋₁, Kᵢ) = REᵢ ⊕ F(LEᵢ, Kᵢ)
```

**這兩條是對的。** 推導：加密時 `REᵢ = LEᵢ₋₁ ⊕ F(REᵢ₋₁, Kᵢ)`，
兩邊同時 XOR 上 `F(REᵢ₋₁, Kᵢ)`，利用 `(a ⊕ b) ⊕ b = a` 就得到
`LEᵢ₋₁ = REᵢ ⊕ F(REᵢ₋₁, Kᵢ)`。再把 `REᵢ₋₁ = LEᵢ` 代進去，
就變成只用得到已知量的形式。

### ⚠️ 書沒講 Feistel 結構最重要的優點

⚠️ **本段不是書上的內容。** 書描述了 Feistel 怎麼運作、也給了解密流程，
**但沒有說出為什麼要用這個結構** —— 而那才是它被 DES 採用的原因。

**輪函式 F 不需要是可逆的。**

看解密公式：它從來沒有計算過 `F⁻¹`。
它需要的只是**再算一次 F**，然後用 XOR 把它消掉。

**這是一個巨大的設計自由。** 你可以把 F 做得任意複雜、任意混亂 ——
查表、位移、非線性替換、任何摧毀結構的操作 ——
完全不必擔心「這個操作能不能反過來做」。

由此得到第二個好處：**加密和解密可以用同一套電路或同一段程式碼**，
差別只在**子金鑰的使用順序相反**（加密 K₁…K₁₆，解密 K₁₆…K₁）。
在 1970 年代硬體很貴的時候，這是決定性的。

> **記住這句話**：Feistel 結構把「可逆性」的責任從 F 身上，
> 轉移到「切兩半 + XOR + 交換」這個外框上。

### 影響 Feistel 網路強度的五個參數

書列了五項，都是「越大／越複雜越安全，但越慢」的權衡：

| 參數 | 書怎麼說 |
|---|---|
| **Block size**（區塊大小） | 越大越安全，但降低加解密速度，要取捨 |
| **Key size**（金鑰長度） | 同樣越大越好，但增加處理時間 |
| **Number of rounds**（輪數） | **單一輪不足以提供安全性**，多輪才行 |
| **Subkey generation algorithm**（子金鑰產生演算法） | 越複雜越難分析；子金鑰要能抵抗暴力破解並提供更好的 confusion |
| **Round function**（輪函式） | 越複雜越難分析 |

> **這五項就是你讀第 5 章 DES 時要盯的五個數字。**
> DES 的答案是：區塊 64 bit、金鑰 56 bit、16 輪。
> 其中**金鑰 56 bit** 就是 DES 後來被淘汰的直接原因。

### ⚠️ 一個容易被誤導的地方：AES 不是 Feistel

⚠️ **本段不是書上的內容，但這個誤解很容易產生。**

書在章首說：

> 📄 **原文**　書 p.45 ｜ PDF p.67
>
> The Data Encryption Standard (DES), Advanced Encryption Standard (AES), etc., are
> examples of block ciphers. Most of the sym­metric ­key-based block cipher algorithms
> currently in use are based on a structure known as Feistel block cipher.

兩句話連著讀，很容易以為 **AES 也是 Feistel 結構。它不是。**

- **DES**（第 5 章）→ Feistel 網路 ✅
- **AES**（第 6 章）→ **Substitution-Permutation Network（SPN，替換排列網路）**

**差別在於**：Feistel 每輪只處理一半的區塊（另一半原封不動搬過去）；
SPN 每一輪處理**整個區塊**。代價是 SPN 的每一個步驟**都必須可逆**，
所以 AES 的解密需要另外一套反向操作，不能像 DES 那樣直接重用加密電路。

> 讀到第 6 章時如果覺得「怎麼跟 DES 長得完全不一樣」，原因就在這裡。

## §4.4 為什麼需要 mode of operation

書 §4.3 ｜ 書頁 49 ｜ PDF 71 ｜ [開啟](./cryptography-cpp.pdf#page=71)

書用一句話點出問題：

> 📄 **原文**　書 p.49 ｜ PDF p.71
>
> What if the size of a message is longer than the considered block size?

**這就是整節的全部動機。**

DES 一次只能加密 64 bit（8 個字元），AES 一次 128 bit（16 個字元）。
你要傳一個 10 MB 的檔案怎麼辦？

**Mode of operation（操作模式）就是「怎麼把一長串資料餵給一個只吃固定大小的函式」的規則。**

書說 **NIST 定義了五種**：ECB、CBC、CFB、OFB、CTR。

⚠️ **這句話在 2001 年是完整的，今天不是。** NIST 後來又定義了好幾種模式，
其中最重要的是 **GCM**（Galois/Counter Mode）——
它是今天 TLS 的預設選擇，也是 **AEAD** 的代表。
**這五種模式全部只提供機密性，不提供完整性**，而 GCM 兩者都給。
詳見本章結尾的缺口表。

## §4.5 ECB —— Electronic Codebook Mode

書 §4.3.1 ｜ 書頁 49–50 ｜ PDF 71–72 ｜ [開啟](./cryptography-cpp.pdf#page=71)

**最簡單的模式：把明文切成 n bit 的區塊，每塊各自獨立加密，用同一把金鑰。**

```
Encryption:  Cᵢ = E_K(Pᵢ)
Decryption:  Pᵢ = D_K(Cᵢ)
```

明文 P₁, P₂, …, P_m → 密文 C₁, C₂, …, C_m。就這樣，沒有別的。

### 唯一的優點

> 📄 **原文**　書 p.49 ｜ PDF p.71
>
> since all the blocks are independent of each other, it does not suffer any
> propagation error.

**區塊彼此獨立，所以錯誤不會擴散** —— 傳輸中某一塊壞了，只有那一塊解不出來。

⚠️ 書沒提到另外兩個附帶好處：**可以完全平行處理**，
而且**可以隨機存取**（想解第 1000 塊不必先解前面 999 塊）。

### 致命缺陷

> 📄 **原文**　書 p.49–50 ｜ PDF p.71–72
>
> If a plaintext block contains two identical n-bit blocks, the corresponding
> ciphertext blocks will be also identical. These regularities provide ­sufficient
> hints to a cryptoanalyst to decipher the message.

**相同的明文區塊 → 相同的密文區塊。**

這是**同一個病，第三次出現**：

| 章節 | 誰保留了結構 |
|---|---|
| 第 2 章 Monoalphabetic | 相同的**字母** → 相同的密文字母 |
| 第 2 章 Playfair | 相同的**雙字母** → 相同的密文對 |
| **第 4 章 ECB** | 相同的**區塊** → 相同的密文區塊 |

**ECB 把單字母替換密碼的錯誤，用 128 bit 的「字母」重犯了一次。**
區塊變大讓它沒那麼容易統計，但性質完全一樣 —— **diffusion 為零**。

### ⚠️ 書漏了最有說服力的示範

⚠️ **本段不是書上的內容。**

ECB 的問題有一個非常有名的視覺化示範（通常叫 **"ECB penguin"**）：
把一張圖片用 ECB 模式加密後，**圖案的輪廓依然清晰可見**——
因為圖片裡大片相同顏色的區域，加密後仍然是大片相同的密文區塊。

書用文字描述了這個問題，但沒有給這個示範。
**這是說明「為什麼 ECB 絕對不能用」最有效的一張圖**，值得自己去找來看。

> **結論：ECB 在任何真實用途上都不該使用。** 書說得比較客氣
> （只說「提供足夠的線索給密碼分析者」），但實務上的共識是：不要用。

## §4.6 CBC —— Cipher Block Chaining

書 §4.3.2 ｜ 書頁 50 ｜ PDF 72 ｜ [開啟](./cryptography-cpp.pdf#page=72)

**IBM 在 1976 年發明，專門用來修 ECB 的問題。**

### 核心想法

> 📄 **原文**　書 p.50 ｜ PDF p.72
>
> every block of the plaintext is XORed with the previous ciphertext block.
> Therefore, identical blocks in the plaintext would not produce identical ciphertext
> blocks.

**每一塊明文先跟「前一塊密文」XOR，再加密。**

因為前一塊密文每次都不同，所以**即使兩塊明文一模一樣，密文也會不同** ——
ECB 的病治好了。

### 第一塊怎麼辦：IV

第一塊明文沒有「前一塊密文」可以用，所以需要一個 **initialization vector（IV，初始向量）**。

書對 IV 的說明：

- **不是秘密**，接收方必須知道它
- **每則訊息應該用不同的 IV**，才能讓每則訊息都獨一無二
- 產生方式必須讓**惡意使用者無法影響它**

```
Encryption:
  C₁ = E_K(P₁ ⊕ IV)
  Cᵢ = E_K(Pᵢ ⊕ Cᵢ₋₁),  i ≥ 2
```

### ⚠️ 書的解密公式是錯的

書上印的是：

```
Decryption:
  P₁ = E_K⁻¹(C₁ ⊕ IV)
  Pᵢ = E_K⁻¹(Cᵢ ⊕ Cᵢ₋₁),  i ≥ 2
```

**XOR 被放進了解密函式的裡面。正確的位置是外面：**

```
  P₁ = D_K(C₁) ⊕ IV
  Pᵢ = D_K(Cᵢ) ⊕ Cᵢ₋₁,  i ≥ 2
```

**推導**：加密是 `C₁ = E_K(P₁ ⊕ IV)`。
先把外層的加密剝掉：`D_K(C₁) = P₁ ⊕ IV`。
再兩邊 XOR 上 IV，用 `(a ⊕ b) ⊕ b = a` 消掉：`P₁ = D_K(C₁) ⊕ IV`。

書上的式子是去解密 `(C₁ ⊕ IV)`，**但被加密的從來就不是那個東西**，算出來是亂碼。

> **書上的圖 4.3(b) 畫的是對的** —— 圖上先過 Decrypt，
> 出來之後才跟 IV／Cₙ₋₁ 做 XOR。**圖對、公式錯。**
> 這是本章最實質的一個錯誤：如果你照公式寫程式，它不會動。

### 代價與風險

**代價：不能平行加密。** 每一塊都要等前一塊的密文算出來。
（解密可以平行，因為所有 Cᵢ 都已經在手上了。）

**風險一：錯誤會擴散。** 書說得很直接 ——

> 📄 **原文**　書 p.50 ｜ PDF p.72
>
> Since the decryption is dependent on the previous block, a single bit error in a
> block will cause the failure.

**風險二：IV 可以被拿來動手腳。** 書指出了一個很重要的攻擊：

> 📄 **原文**　書 p.50 ｜ PDF p.72
>
> if someone predictably changes bits in IV intentionally, the corresponding bits of
> the received value of P₁ can be changed.

**攻擊者翻轉 IV 裡的某個 bit，解密後 P₁ 的對應 bit 就跟著翻轉。**
因為 P₁ = D_K(C₁) ⊕ IV，改 IV 等於直接改 P₁。

⚠️ **書只講了 IV 這一個位置，但同樣的手法對所有區塊都成立** ——
翻轉 Cᵢ 的某個 bit，會讓 P_{i+1} 的對應 bit 翻轉
（代價是 Pᵢ 整塊變成亂碼）。這叫 **bit-flipping attack**。

### ⚠️ 書講了現象，但沒講結論

⚠️ **本段不是書上的內容。**

上面那個攻擊是整章最重要的一件事，因為它證明了：

> **加密（機密性）完全不保證完整性。**
> 攻擊者看不懂內容，但**可以有目的地修改它**。

書描述了這個現象，卻**沒有說出解法**。解法是：加密之外還要加上
**MAC（訊息認證碼）**，或直接使用同時提供兩者的 **AEAD 模式**。

**而這本書全書沒有 MAC 專章、也沒有 AEAD。**
這是第 1 章缺口表列的第一項，在這裡具體現形了。

### ⚠️ 書對 IV 的要求說得不夠

書說 IV「必須讓惡意使用者無法影響它」。**這不夠。**

⚠️ **本段不是書上的內容。** CBC 的 IV 還必須是**不可預測的**（隨機的）。
如果攻擊者能**預測**下一個 IV（即使他無法影響它），
就能發動選擇明文攻擊。這是後來 TLS 1.0 的 BEAST 攻擊的成因之一。

**三個要求：不必保密、每則訊息不重複、且不可預測。** 書只說了前兩個半。

## §4.7 CFB —— Cipher Feedback Mode

書 §4.3.3 ｜ 書頁 50–52 ｜ PDF 72–74 ｜ [開啟](./cryptography-cpp.pdf#page=72)

### 它在解什麼問題

ECB 和 CBC 都要求**完整的區塊**。資料不夠一塊時就得補 **padding**。

**CFB 讓區塊密碼表現得像串流密碼** ——

> 📄 **原文**　書 p.51 ｜ PDF p.73
>
> Unlike the ECB and CBC, the CFB mode is a stream cipher. One desirable property of
> a stream cipher is that it produces the ciphertext of the same length as the
> plaintext.

**密文長度等於明文長度，不需要 padding。**

### 運作方式

除了 IV 之外，CFB 還需要一個參數 **s**，代表**每次傳輸的單位**（多少 bit）。

書描述的流程（對照圖 4.4）：

1. 第一個輸入區塊是 **IV**，對它做**加密**運算，得到第一個輸出區塊
2. **只保留最高的 s 個 bit**，其餘 n − s 個 bit **丟棄**
3. 這 s 個 bit 跟第一段 s bit 的明文 XOR，得到第一段密文
4. 產生下一個輸入區塊：把暫存器**左移 s 個 bit**，
   **把剛產生的那段密文填進最低的 s 個 bit**
5. 重複，直到所有明文段都處理完

### ⚠️ 解密也用加密函式 —— 這點書講對了，而且很重要

> 📄 **原文**　書 p.52 ｜ PDF p.74 ｜ [開啟](./cryptography-cpp.pdf#page=74)
>
> Note that there is no decryption function utilized to decrypt a ciphertext, but an
> encryption function is used.

**CFB 解密時完全不用 D_K，只用 E_K。**

為什麼？因為區塊密碼在這裡**不是拿來加密明文的**，
而是拿來**產生金鑰流**的。明文跟金鑰流之間的運算是 XOR ——
而 XOR 自己就是自己的反運算（`(a ⊕ b) ⊕ b = a`，見 §4.2）。

> **這是理解 CFB / OFB / CTR 三個模式的鑰匙**：
> 它們都是「用區塊密碼造一個金鑰流，再跟明文 XOR」。
> **區塊密碼被降格成一個虛擬亂數產生器。**
> 回頭看第 1 章圖 1.1 的串流密碼流程圖 —— 就是同一張圖。

### ⚠️ 書上的公式下標錯了兩處

書上印的是：

```
Encryption:  C₁ = E_K(IV) ⊕ P₁
             Cᵢ = E_K(Cᵢ₋₁) ⊕ P₁,  i ≥ 2      ← 應為 Pᵢ
Decryption:  P₁ = E_K(IV) ⊕ C₁
             Pᵢ = E_K(Cᵢ₋₁) ⊕ C₁,  i ≥ 2      ← 應為 Cᵢ
```

**兩條 `i ≥ 2` 的式子右邊都寫成了下標 1**，應該是下標 i。
照字面讀的話，第 2 塊之後的所有密文都是拿**第一塊明文**去加密 —— 顯然不對。

（書上的圖 4.4(b) 裡，第二段的密文標籤看起來也印成了 C₁，應為 C₂ ——
同一個下標混亂在圖和公式裡各出現一次。）

### 缺點

> 📄 **原文**　書 p.53 ｜ PDF p.75
>
> The CFB suffers from error propagation since all the ciphertext segments are
> related to each other.

**錯誤會擴散**，因為密文段之間互相關聯（前一段密文是下一段的輸入）。

## §4.8 OFB —— Output Feedback Mode

書 §4.3.4 ｜ 書頁 53 ｜ PDF 75 ｜ [開啟](./cryptography-cpp.pdf#page=75)

**結構跟 CFB 幾乎一樣，只差一條線接在哪裡。**

> 📄 **原文**　書 p.53 ｜ PDF p.75
>
> Unlike the CFB, the ciphertext segment is not fed back to the next input block.
> Instead, the output of the encryption function is fed back to the next input block.

| | 回饋什麼給下一個輸入區塊 |
|---|---|
| **CFB** | **密文**段 |
| **OFB** | **加密函式的輸出**（也就是金鑰流本身） |

```
Encryption:  s₁ = E_K(IV),      C₁ = s₁ ⊕ P₁
             sᵢ = E_K(sᵢ₋₁),    Cᵢ = sᵢ ⊕ Pᵢ,  i ≥ 2
```

### 這條線改在哪裡，差別很大

⚠️ **本段是我的整理，書沒有明講這個推論。**

因為金鑰流 `s₁, s₂, s₃, …` **完全不依賴明文或密文**，只依賴 IV 和金鑰，所以：

1. **金鑰流可以事先算好**（在明文還沒出現之前就先產生一整串）
2. **錯誤不會擴散** —— 密文某個 bit 壞掉，只影響明文對應的那個 bit
3. 但也因此 —— **攻擊者可以做精準的 bit 翻轉**

書講了第三點：

> 📄 **原文**　書 p.53 ｜ PDF p.75
>
> Since all the ciphertext segments are independent of each other, this mode is more
> vulnerable to a message stream modification attack than CFB.

**OFB 比 CFB 更容易被「訊息串流修改攻擊」。**
在 CFB 裡改一個 bit 會把後面搞爛（攻擊者不容易控制結果）；
在 OFB 裡改一個 bit 就**只**改那一個 bit —— 完全可控。

> 又是 §4.6 那個結論：**機密性不等於完整性。**

### ⚠️ 書上的解密公式整組寫錯了

書上印的是：

```
Decryption:  s₁ = E_K(IV),      C₁ = (s₁ ⊕ C₁)      ← 左邊應為 P₁
             sᵢ = E_K(sᵢ₋₁),    Cᵢ = (sᵢ ⊕ Cᵢ)      ← 左邊應為 Pᵢ
```

**兩條式子的左邊都寫成了 C，應該是 P。** 照字面讀是
`C₁ = s₁ ⊕ C₁` —— 一個自我指涉、不成立的式子。

正確應為：

```
             P₁ = s₁ ⊕ C₁
             Pᵢ = sᵢ ⊕ Cᵢ
```

**這是本章第二個會讓人照著寫不出東西的錯誤**（第一個是 §4.6 的 CBC 解密）。

### ⚠️ 書沒講 OFB 最危險的地方

⚠️ **本段不是書上的內容。**

**IV 絕對不能重複使用。**

因為金鑰流只由 (K, IV) 決定，同一組 (K, IV) 會產生**完全相同的金鑰流**。
兩則訊息用同一串金鑰流的話：

```
C ⊕ C' = (s ⊕ P) ⊕ (s ⊕ P') = P ⊕ P'
```

**金鑰流被消掉了** —— 攻擊者不需要金鑰，光靠兩則密文就能得到兩則明文的 XOR。
這叫 **two-time pad**，是串流密碼最經典的災難。

同樣的風險對 §4.9 的 CTR 模式也成立，而且更嚴重。**書兩處都沒有警告。**

## §4.9 CTR —— Counter Mode

書 §4.3.5 ｜ 書頁 53–55 ｜ PDF 75–77 ｜ [開啟](./cryptography-cpp.pdf#page=75)

**最簡單、也是今天最常用的模式。**

### 運作方式

**不回饋任何東西 —— 改用一個計數器。**

> 📄 **原文**　書 p.53 ｜ PDF p.75
>
> In general, the counter is initialized to some value that is then incremented by 1
> for every subsequent block.

每一塊配一個**互不相同**的計數器值，計數器加密後的結果跟明文 XOR：

```
Encryption:  Cᵢ = E_K(CTRᵢ) ⊕ Pᵢ
Decryption:  Pᵢ = E_K(CTRᵢ) ⊕ Cᵢ
```

**加密和解密是同一條式子**（因為 XOR 自逆）。

### 兩個關鍵優點

書列了兩個，都很重要：

> 📄 **原文**　書 p.55 ｜ PDF p.77 ｜ [開啟](./cryptography-cpp.pdf#page=77)
>
> both the CTR encryption and the CTR decryption can be parallelized since the second
> encryption can begin before the first one has finished. Moreover, if necessary, any
> particular cipher­text block/plaintext block can be recovered independently if the
> corresponding counter block can be determined.

1. **完全可平行化** —— 每一塊的金鑰流只取決於它自己的計數器值，
   不必等前一塊。**加密和解密都可以平行**（CBC 只有解密可以）。
2. **可隨機存取** —— 想解開第 1000 塊，直接算 `E_K(CTR₁₀₀₀)` 就好，
   不必先處理前面 999 塊。

> **這兩點就是為什麼 CTR 成為現代主流。**
> 今天的 **GCM** 模式（TLS 的預設）核心就是 CTR，
> 外面再加上一層認證標籤。

### ⚠️ 書上的圖 4.6(b) 畫錯了

**圖 4.6(b)「Decryption」把計數器餵給一個標示為 `Decrypt` 的方塊。**

**應該是 `Encrypt`。**

證據是**書自己的公式**：`Pᵢ = E_K(CTRᵢ) ⊕ Cᵢ` —— 用的是 **E_K**，不是 D_K。

而且書在 §4.3.3 講 CFB 時才剛親口說過
「there is no decryption function utilized to decrypt a ciphertext, but an
encryption function is used」——**同樣的道理完全適用於 CTR**，
但圖卻畫反了。

> **公式對、圖錯。** 剛好跟 §4.6 的 CBC 相反（那裡是圖對、公式錯）。

### ⚠️ 書完全沒有警告計數器不可重複

⚠️ **本段不是書上的內容。**

跟 OFB 一樣，**同一把金鑰下，計數器值絕對不可以重複使用**，
否則就是 §4.8 講的 two-time pad 災難。

**而 CTR 的風險比 OFB 更高**，因為計數器是**可預測的遞增值** ——
如果兩則訊息都從 0 開始數，它們的金鑰流會**完全重疊**。

實務上的做法是把計數器分成兩段：一段是每則訊息都不同的 **nonce**，
一段才是遞增的計數器。**書把整個計數器籠統地說成「初始化成某個值然後遞增」，
沒有提 nonce，也沒有提重複使用的後果。**

## §4.10 五種模式放在一起看

⚠️ **本節是我加的整理表，不是書上的章節。**

| 模式 | 怎麼串 | 需要 IV | 需 padding | 加密可平行 | 解密可平行 | 錯誤擴散 | 用 D_K 嗎 |
|---|---|---|---|---|---|---|---|
| **ECB** | 不串 | ❌ | ✅ | ✅ | ✅ | 不擴散 | ✅ |
| **CBC** | 前一塊**密文** XOR 進下一塊明文 | ✅ | ✅ | ❌ | ✅ | 會擴散 | ✅ |
| **CFB** | 前一段**密文**回饋進暫存器 | ✅ | ❌ | ❌ | ✅ | 會擴散 | ❌ |
| **OFB** | 前一段**金鑰流**回饋進暫存器 | ✅ | ❌ | ❌ | ❌ | 不擴散 | ❌ |
| **CTR** | 不串，用**計數器** | ✅（nonce） | ❌ | ✅ | ✅ | 不擴散 | ❌ |

### 三個看表的重點

**1. 後三種模式把區塊密碼變成了串流密碼。**
CFB、OFB、CTR 都不用 `D_K`，因為區塊密碼在那裡只負責**產生金鑰流**，
真正的加解密是 XOR。**這也是它們不需要 padding 的原因** ——
金鑰流要多長就取多長。

**2. 「錯誤不擴散」是一把雙面刃。**
OFB 和 CTR 錯誤不擴散，聽起來是優點（傳輸品質差的環境很有用），
但它同時代表**攻擊者可以做精準的、可控的修改**。

**3. 五種模式沒有一種提供完整性。**
這是整章最需要記住的一句話，也是下一節的主題。

## ⚠️ 第 4 章的問題總表

| 位置 | 問題 | 嚴重度 |
|---|---|---|
| §4.3.2 CBC | **解密公式把 XOR 放進解密函式裡面**，應為 `Pᵢ = D_K(Cᵢ) ⊕ Cᵢ₋₁`（圖 4.3 是對的） | **嚴重** |
| §4.3.4 OFB | **解密公式左邊寫成 C，應為 P**，成為自我指涉的式子 | **嚴重** |
| §4.3.5 CTR | **圖 4.6(b) 畫成 `Decrypt`**，應為 `Encrypt`（公式是對的） | 高 |
| §4.3.3 CFB | 公式兩處下標錯：`⊕ P₁` 應為 `⊕ Pᵢ`、`⊕ C₁` 應為 `⊕ Cᵢ`；圖 4.4(b) 標籤同樣混亂 | 高 |
| §4.2 Feistel | XOR 用 `⊗` 而非 `⊕`；同一章 §4.3 卻用對了 | 中（符號不一致） |
| §4.1 Confusion | `"loosened"` 與同段的 `"as complex as possible"` 矛盾 | 中 |
| §4.1 Diffusion | 定義句末 `"ciphertext characters"` 應為 `"plaintext characters"`，成為循環定義 | 中 |
| §4.1 | Shannon 拼成 **"Calude"**（參考文獻裡是對的） | 低 |
| 章首 | 「第 3 章的密碼都是串流密碼」—— 應為第 2、3 章 | 低 |
| 章首 | 「區塊密碼一般比串流密碼安全」—— 無根據的通則 | 中（觀念偏誤） |
| §4.2 | 沒說 Feistel 的核心優點：**F 不需可逆、加解密共用電路** | 中（深度） |
| 章首 | 未澄清 **AES 不是 Feistel 而是 SPN**，兩句話連讀易生誤解 | 中（深度） |

### 這章沒有的東西

| 缺什麼 | 為什麼要緊 |
|---|---|
| **AEAD / GCM / CCM** | **這是本章最大的缺口。** 五種模式全部只給機密性；今天的預設做法是 AEAD（同時給機密性與完整性）。GCM 全書 2 次、AEAD 全書 0 次 |
| **MAC / HMAC** | §4.3.2 的 bit-flipping 攻擊直接指向它，書描述了現象卻沒說解法 |
| **Padding 的細節** | §4.3.3 只用一個子句帶過「padding bits are affixed」，沒有講任何 padding 方案（如 PKCS#7），也沒有 padding oracle 攻擊 |
| **IV 必須不可預測** | 書只說「不可被惡意使用者影響」，漏掉「不可預測」這個 CBC 的硬性要求 |
| **Nonce 重用的災難** | OFB 和 CTR 兩節都沒有警告 two-time pad |
| **ECB penguin** | 說明 ECB 為何不可用最有力的示範，書沒有 |

## 📌 第 4 章的三句話重點

1. **Shannon 的 confusion 與 diffusion 是第 2 章教訓的正式化** ——
   古典密碼全部死於 diffusion 不足（明文的統計結構原封不動留在密文裡）。
2. **Feistel 結構的價值在於「輪函式 F 不需要可逆」** ——
   可逆性由「切兩半 + XOR + 交換」的外框保證，
   所以 F 可以任意複雜，加解密還能共用同一套電路。（⚠️ 書沒說這點。）
3. **五種操作模式沒有一種提供完整性** ——
   書自己示範的 CBC bit-flipping 攻擊就證明了「看不懂」不等於「改不了」，
   但書沒有給出解法（MAC 或 AEAD），而全書都沒有。

## 📖 第 4 章名詞小抄

| 英文 | 中文 | 一句話 |
|---|---|---|
| Block cipher | 區塊密碼 | 一次加密固定大小的一整塊，輸出等長 |
| XOR (⊕) | 互斥或 | 相同得 0、不同得 1；`(a⊕b)⊕b = a`，所以自己是自己的反運算 |
| Confusion | 混淆 | 讓**金鑰與密文**的關係盡可能複雜（手段：替換） |
| Diffusion | 擴散 | 讓**明文的統計結構**散佈到整個密文（手段：排列） |
| Feistel network | Feistel 網路 | 切兩半、多輪、每輪 `LEᵢ=REᵢ₋₁`、`REᵢ=LEᵢ₋₁⊕F(REᵢ₋₁,Kᵢ)` |
| Round | 回合 | Feistel 的一輪；DES 有 16 輪 |
| Subkey / Round key | 子金鑰／回合金鑰 | 由主金鑰推導、每輪各一把 |
| Round function (F) | 輪函式 | Feistel 每輪的加工函式；**不需要可逆** |
| SPN | 替換排列網路 | AES 用的結構，每輪處理整個區塊（⚠️ 不是 Feistel） |
| Mode of operation | 操作模式 | 把長訊息餵給定長區塊密碼的規則 |
| ECB | 電子碼簿模式 | 每塊獨立加密；相同明文塊→相同密文塊，**不可使用** |
| CBC | 密碼區塊鏈接模式 | 明文先 XOR 前一塊密文再加密；需要 IV |
| CFB | 密文回饋模式 | 回饋**密文**；變成串流密碼，不需 padding |
| OFB | 輸出回饋模式 | 回饋**金鑰流**；錯誤不擴散，金鑰流可預先計算 |
| CTR | 計數器模式 | 加密計數器產生金鑰流；**可平行、可隨機存取** |
| IV (Initialization Vector) | 初始向量 | 第一塊用的起始值；不必保密，但須不重複**且不可預測** |
| Nonce | 一次性數值 | 每則訊息不同的值；CTR 的計數器高位段（⚠️ 書未提） |
| Padding | 填充 | 資料不足一整塊時補到足量（⚠️ 書僅一句帶過） |
| Error propagation | 錯誤擴散 | 一個 bit 的錯誤影響到後續區塊 |
| AEAD | 認證式加密 | 同時提供機密性與完整性（⚠️ 全書 0 次） |

---
---

# 📕 非目標：第 12～14 章是什麼、什麼時候再回來讀

這三章佔全書四分之一（書頁 225–337 ｜ PDF 247–359），
但**調性與前 11 章完全不同** —— 前 11 章是教科書，這三章是研究論文。
依 [brief](./cryptography-cpp-notes-brief.md) §4，本筆記**不寫它們的內容**。

### 第 12 章 Fundamentals of Identity-Based Cryptography
書頁 225 ｜ PDF 247 ｜ 作者 Aymen Boudguiga、Maryline Laurent、Mohamed Hamdi

**還算密碼學觀念**：用「電子郵件地址」這種公開的身分字串**直接當公鑰**，
免去憑證的麻煩（回想第 1 章 §1.7 的 CA 與憑證鏈）。

**前置知識**：雙線性配對（bilinear pairing）、橢圓曲線群 ——
也就是說，**至少要先讀完第 9 章 ECC**。

**什麼時候回來**：讀完第 9 章、而且你對「憑證為什麼這麼麻煩」有實際感受之後。

### 第 13 章 Symmetric Key Encryption Acceleration on Heterogeneous Many-Core Architectures
書頁 251 ｜ PDF 273 ｜ 作者 Giovanni Agosta 等四人（義大利米蘭理工）

**這章不是密碼學，是高效能運算。** 主題是怎麼用 GPU／多核心加速對稱加密，
內容大量是 C++ template 特化與 OpenCL/CUDA 的架構設計。

**前置知識**：第 6 章 AES、C++ template metaprogramming、GPU 程式設計。

**什麼時候回來**：你有一個**實際的效能問題**要解的時候。純學習密碼學不需要它。

### 第 14 章 Methods and Algorithms for Fast Hashing in Data Streaming
書頁 299 ｜ PDF 321 ｜ 作者 Marat Zhanikeev

**這章的 hashing 跟第 10、11 章的不是同一件事。**
第 10、11 章講的是**密碼學雜湊**（MD5、SHA，目標是抗碰撞）；
這章講的是**資料串流處理**裡的快速雜湊（目標是速度與統計估計）。

**注意不要混淆這兩種 hash** —— 名字一樣，目標完全相反。

**什麼時候回來**：做網路量測或串流資料分析的時候。

---

## 進度

| 章 | 標題 | 書頁 | PDF 頁 | 狀態 |
|---|---|---|---|---|
| 1 | 資訊安全與密碼學基礎 | 1–10 | 23–32 | ✅ 完成 |
| 2 | 古典密碼演算法 | 11–34 | 33–56 | ✅ 完成 |
| 3 | 轉輪機 | 35–44 | 57–66 | ✅ 完成 |
| 4 | 區塊密碼 | 45–56 | 67–78 | ✅ 完成 |
| 5 | Data Encryption Standard | 57–90 | 79–112 | ⬜ |
| 6 | Advanced Encryption Standard | 91–126 | 113–148 | ⬜ |
| 7 | Asymmetric Key Algorithms | 127–134 | 149–156 | ⬜ |
| 8 | The RSA Algorithm | 135–146 | 157–168 | ⬜ |
| 9 | Elliptic Curve Cryptography | 147–182 | 169–204 | ⬜ |
| 10 | Message Digest Algorithm 5 | 183–206 | 205–228 | ⬜ |
| 11 | Secure Hash Algorithm | 207–224 | 229–246 | ⬜ |
| 12–14 | — | 225–337 | 247–359 | ❌ 非目標 |
