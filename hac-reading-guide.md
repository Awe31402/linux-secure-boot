# 導讀：Handbook of Applied Cryptography

> A. Menezes, P. van Oorschot, S. Vanstone, *Handbook of Applied Cryptography*,
> CRC Press, 1996。合併版 PDF 共 **803 頁**。
> 原始檔：[handbook-of-applied-cryptography.pdf](./handbook-of-applied-cryptography.pdf)
> 規格見 [hac-reading-guide-brief.md](./hac-reading-guide-brief.md)。
>
> **這份東西是導航，不是教材。** 它不解釋密碼學，它告訴你這本書要怎麼走：
> 哪些先讀、哪些跳過、讀某一節之前要先補什麼。
> 如果你讀完這份覺得「懂了，不用看書了」，那它就失敗了。
>
> **出處標示**：引用書上的話時附一段 📄 **原文**（不翻譯），標**書頁**（印在紙上的）
> 與 **PDF 頁**（這個合併檔的第幾頁）；節末再放一行 📖 範圍與可點連結。
>
> ⚠️ 兩者的差值**不固定**（+10 到 +23）。完整換算表見
> [crypto-course-notes-brief.md](./crypto-course-notes-brief.md)，
> 本檔所有 PDF 頁碼都是照那張表換算的。
>
> **語言**：中文為主，專有名詞保留英文（查索引時要對得上）。

**本輪範圍**：§0、§1 全書地圖、§2 的**一站樣板**。其餘見文末〈本輪沒做什麼〉。

---

## §0 讀這本書之前

> ⚠️ 本節不是書上的內容，是定位說明。

### §0.1 這本書不是教科書，是工具書

書名裡的 **Handbook** 是認真的。它的編排目標是「查得到」，不是「讀得順」——
所以它會先把工具全部倒在桌上，再開始做事。

這對你的影響很具體。看目錄的頁碼：

| 你讀完 | 下一個**具體的密碼系統**在哪 | 中間隔了多遠 |
|---|---|---|
| 第 1 章（書頁 1–48） | 第 6 章 Stream Ciphers（書頁 191） | **第 2–5 章，142 頁** |

那 142 頁是：機率／資訊理論／複雜度／數論／抽象代數（第 2 章）、
數論難題與各種分解演算法（第 3 章）、質數產生（第 4 章）、亂數（第 5 章）。

作者自己在第 2 章開頭就講明了它的性質：

> 📄 **原文**　書 p.49 ｜ PDF p.60
>
> This chapter is a collection of basic material on probability theory, information
> theory, complexity theory, number theory, abstract algebra, and finite fields
> that will be used throughout this book.

**a collection of basic material** —— 這是工具箱的自我描述，不是課程。
工具箱要用查的，不是從第一格讀到最後一格。

**照書序線性讀的下場**：你會在還沒看過任何一個真的加密系統之前，
先吃掉 142 頁抽象數學，然後放棄。這不是你的問題，是書的編排方式跟
「初學者第一次讀」這個用途不合。

### §0.2 這份導讀怎麼用

**把第 2、3 章從路線上拿掉，改成隨叫隨到。**

- **[§1 全書地圖](#1-全書地圖)**：15 章分成**主線**與**非主線**。
  主線是一條 7 站的路，照它走。非主線的章各有一句話 +
  「什麼時候該回來讀它」，在那之前不要碰。
- **[§2 主線各站](#2-主線各站)**：每站六格，其中最重要的是
  **② 讀之前先補**——它會把第 2、3 章拆成「這站只需要這幾頁」。

**這份導讀不會告訴你答案，只會告訴你去哪裡找答案。** 六格裡的
「③ 精讀」指的是**你要真的翻開書讀那幾頁**。

### §0.3 兩件先講清楚的事

**① 這個合併 PDF 少了 Foreword 和 Preface。**
目錄列出 Rivest 的 Foreword（書頁 xxi）與作者 Preface（書頁 xxiii），
但合併檔裡**沒有**——PDF 第 1–9 頁是目錄，第 10 頁是 CRC 授權聲明，
第 11 頁直接跳進第 1 章。

意思是**作者自己寫的「這本書怎麼讀」不在你手上**。
好消息是每章的 §x.1 裡都有一段 **Chapter outline**，作者在那裡逐節說明
「哪一節在幹嘛、為什麼收錄」。本導讀的取捨判斷主要靠那些段落，不靠猜。

**② 這本書是 1996 年的。**
概念骨架沒有過期，**過期的是具體演算法清單**。導讀會在對應位置放
一行 ⚠️ 標記，完整清單留給文末的〈這本書哪些地方老了〉總表（下一輪補）。

---

## §1 全書地圖

### §1.1 主線：7 站

照這個順序走。**這 7 站以外的章，在被某一站的「② 讀之前先補」點名之前，
一律不要碰。**

| 站 | 章 | 標題 | 書頁 | PDF 頁 | 這站給你什麼 |
|---|---|---|---|---|---|
| **1** | 1 | Overview of Cryptography | 1–48 | 11–59 | 全書的地圖與詞彙。作者明說這章是 tutorial |
| **2** | 7 | Block Ciphers | 223–282 | 239–299 | 對稱加密實際長什麼樣、模式（ECB/CBC…）在解什麼 |
| **3** | 8 | Public-Key Encryption | 283–320 | 300–337 | 公鑰的兩大家族：分解難題（RSA）與離散對數（ElGamal） |
| **4** | 9 | Hash Functions and Data Integrity | 321–384 | 338–401 | 雜湊與 MAC，以及「完整性」到底怎麼保證 |
| **5** | 11 | Digital Signatures | 425–488 | 443–507 | 簽章＝公鑰＋雜湊的組合拳 |
| **6** | 12 | Key Establishment Protocols | 489–542 | 508–561 | 兩邊怎麼協商出一把共用金鑰（含 Diffie-Hellman） |
| **7** | 13 | Key Management Techniques | 543–590 | 562–610 | 憑證、CA、信任模型、金鑰生命週期 |

主線總計約 **340 書頁**，但實際要**精讀**的遠少於此——每站的「③ 精讀」會標明。

**為什麼是這個順序**：這是書本身的順序（1 → 7 → 8 → 9 → 11 → 12 → 13），
沒有重排。導讀動的不是這幾章的先後，而是**把第 2–6 章與第 10 章從主線上移開**。
第 1 章之後直接跳到第 7 章，是這條路線唯一的大動作。

### §1.2 非主線：8 章，什麼時候回來讀

| 章 | 標題 | 書頁 | PDF 頁 | 一句話 | 什麼時候回來讀 |
|---|---|---|---|---|---|
| 2 | Mathematical Background | 49–86 | 60–98 | 工具箱：機率、資訊理論、複雜度、數論、代數、有限體 | **永遠不通讀。** 被某站的「② 讀之前先補」點名時，只讀被點名的那幾頁 |
| 3 | Number-Theoretic Reference Problems | 87–132 | 99–145 | 公鑰安全性所依賴的「難題清單」＋破解它們的演算法 | 走到站 3（第 8 章）時，照書頁 284 的 **Table 8.1** 回來查對應小節，**只讀難題的定義，跳過分解演算法** |
| 4 | Public-Key Parameters | 133–168 | 146–182 | 怎麼生出大質數與其他公鑰參數（Miller-Rabin 等） | 站 3 讀完，開始問「那些質數到底怎麼來的」時，讀 §4.2.3（Miller-Rabin）與 §4.4.1 |
| 5 | Pseudorandom Bits and Sequences | 169–190 | 183–205 | 亂數與偽亂數的產生與品質檢驗 | 開始問「金鑰的隨機性從哪來、不夠隨機會怎樣」時，讀 §5.1 與 §5.5 |
| 6 | Stream Ciphers | 191–222 | 206–238 | 串流密碼，內容以 LFSR 為主 | ⚠️ 這章的時代落差很大（見文末總表）。第一遍**只瀏覽 §6.1**，知道 stream 與 block 的差別即可 |
| 10 | Identification and Entity Authentication | 385–424 | 402–442 | 密碼、挑戰-回應、零知識識別協定 | 站 5（簽章）讀完，想分清「認人」與「認訊息」的差別時，讀 §10.1 與 §10.3 |
| 14 | Efficient Implementation | 591–634 | 611–655 | 大數運算、Montgomery 約簡、快速冪 | **要動手寫程式時才讀。** 純理解骨架用不到 |
| 15 | Patents and Standards | 635–662 | 656–683 | 1996 年的專利與標準快照 | ⚠️ 全書時代落差最大的一章。當**史料**讀，不要當現況 |

### §1.3 不是章的部分

| 部分 | PDF 頁 | 說明 |
|---|---|---|
| 附錄 A（Bibliography of Papers…） | 684–724 | 1996 年前的研討會論文清單。查文獻用 |
| References | 725–777 | 參考文獻 |
| **Index** | **778–803** | **這本書當工具書用的正門。** 讀到不認識的名詞，先查這裡，比翻目錄快 |

### §1.4 這本書自己怎麼定位第 1 章

> 📄 **原文**　書 p.2 ｜ PDF p.12
>
> Chapter 1 is a tutorial on the many and various aspects of cryptography. It does
> not attempt to convey all of the details and subtleties inherent to the subject.
> Its purpose is to introduce the basic issues and principles and to point the reader
> to appropriate chapters in the book for more comprehensive treatments. Specific
> techniques are avoided in this chapter.

作者自己說第 1 章是 **tutorial**、而且**刻意避開具體技術**。
所以站 1 讀起來會很輕——那是設計如此，不是你讀得不夠深。
它的任務是給你詞彙表和索引感，不是給你能力。

📖 **書頁 1–48** ｜ PDF 頁 11–59 ｜ [開啟 PDF](./handbook-of-applied-cryptography.pdf#page=11)

---

## §2 主線各站

> **本輪只寫了站 3 當格式樣板。** 站 1、2、4–7 下一輪補。
>
> **為什麼樣板挑站 3 而不是站 1**：站 1（第 1 章）沒有前置依賴、
> 也幾乎沒有可跳過的東西——拿它當樣板，六格裡最重要的
> ②「讀之前先補」和 ④「可以跳過」會是空的，驗證不了格式好不好用。
> 站 3（第 8 章 公鑰加密）是主線上依賴最重、取捨最多的一站，
> 格式在這裡站得住，其他站就都沒問題。

### 站 3｜第 8 章 Public-Key Encryption

**全章 38 書頁（283–320）｜PDF 300–337｜建議精讀約 13 頁**

#### ① 這站在解什麼問題

對稱加密有一個沒解決的前提：**兩邊得先有同一把鑰匙**。鑰匙怎麼送過去？

這一章就是答案的一半——**把加密和解密拆成兩把不同的鑰匙**，加密那把可以公開。
另一半（怎麼確認你拿到的公鑰真的是對方的）在站 6、站 7。

這章的重點不是「RSA 怎麼算」，而是**公鑰加密的安全性是怎麼掛在一個數學難題上的**：
RSA 掛在「分解大整數很難」，ElGamal 掛在「離散對數很難」。
這個「掛」的動作本身，才是這章要你學會的思考方式。

#### ② 讀之前先補

書頁 284（PDF 301）的 **Table 8.1** 是這章的依賴總表——
作者自己列出每個公鑰方案的安全性建立在第 3 章的哪個問題上。先看那張表。

**第 3 章（書上明講的依賴）**

| 補什麼 | 書頁 | PDF 頁 | 為什麼需要它 |
|---|---|---|---|
| §3.2 開頭（只讀第一頁） | 89 | 101 | 知道 FACTORING 問題的定義、以及哪些方案依賴它。**§3.2.1–3.2.7 七種分解演算法全部跳過** |
| §3.3 The RSA problem | 98–99 | 110–111 | 只有 1 頁多。「RSA 問題」跟「分解問題」不是同一件事，這頁講清楚差別 |
| §3.6 開頭（只讀定義） | 103 | 115 | 離散對數問題的定義，§8.4 ElGamal 要用。**§3.6.1–3.6.6 的求解演算法跳過** |

**第 2 章（書上沒明講，這是本導讀的判斷）**

> ⚠️ 以下這幾條不是書上寫的依賴，是實際翻過 §8.2 之後、
> 依它引用到的 Algorithm 與 Fact 編號回推的。

| 補什麼 | 書頁 | PDF 頁 | 為什麼需要它 |
|---|---|---|---|
| §2.4.3 The integers modulo n | 67–71 | 78–82 | 整章 RSA 都在 $\mathbb{Z}_n$ 裡算。Euler phi 函數 $\phi(n)$、Fermat 定理（Fact 2.127）、CRT（Fact 2.120）都在這 5 頁 |
| §2.4.2 Algorithms in $\mathbb{Z}$ | 66–67 | 77–78 | RSA 金鑰產生的第 4 步要用 extended Euclidean algorithm（Algorithm 2.107）算 $d$ |
| §2.4.4 Algorithms in $\mathbb{Z}_n$ | 71–72 | 82–83 | 加解密要用 repeated square-and-multiply（Algorithm 2.143）算模冪 |

**合計前置約 11 頁。** 這就是「不用先啃 142 頁數學」的具體意思。

#### ③ 精讀

| 讀什麼 | 書頁 | PDF 頁 | 約 | 重點 |
|---|---|---|---|---|
| §8.1 Introduction ＋ Chapter outline | 283–284 | 300–301 | 2 頁 | 公鑰加密的一般框架；Table 8.1 依賴表 |
| §8.2 開頭 ＋ §8.2.1 Description | 285–287 | 302–304 | 3 頁 | Algorithm 8.1 金鑰產生、Algorithm 8.3 加解密、**Example 8.4 小參數實例** |
| §8.2.2 的 (i)(ii)(iii) | 287–288 | 304–305 | 2 頁 | (i) 跟分解的關係、(ii) 小 $e$ 的風險、(iii) forward search attack |
| §8.2.3 RSA encryption in practice | 290–292 | 307–309 | 3 頁 | 模數大小、質數怎麼選、$e$ 怎麼選 |
| §8.4.1 Basic ElGamal encryption | 294–297 | 311–314 | 3 頁 | 離散對數家族的代表。**不能跳**——站 5 的 DSA、站 6 的 DH 都從這裡長出來 |

> **Example 8.4（書頁 287｜PDF 304）的參數小到可以手算。**
> 拿紙筆把金鑰產生 → 加密 → 解密整條跑一次。這一步做了，RSA 就是你的；
> 沒做，讀十遍還是別人的。

#### ④ 可以跳過

| 跳什麼 | 書頁 | PDF 頁 | 理由 |
|---|---|---|---|
| §8.2.2 的 (iv)–(viii) | 288–290 | 305–307 | small decryption exponent、multiplicative properties、common modulus、cycling、message concealing——都是特定情境的攻擊，第一遍不影響理解骨架 |
| §8.3 Rabin | 292–294 | 309–311 | 理論漂亮（安全性可證明等價於分解），實務上沒人用 |
| §8.4.2 Generalized ElGamal | 297–298 | 314–315 | 把 ElGamal 推廣到任意循環群。要先熟 §8.4.1 才有意義 |
| §8.5 McEliece | 298–300 | 315–317 | 1996 年的冷門方案 |
| §8.6 Knapsack | 300–306 | 317–323 | **作者自己說了跳過的理由**（見下方原文） |
| §8.7 Probabilistic public-key encryption | 306–312 | 323–329 | 概念重要但偏理論，第二遍再讀 |
| §8.8 Notes and further references | 312–320 | 329–337 | 8 頁參考文獻，查資料時才用 |

> 📄 **原文**　書 p.284 ｜ PDF p.301
>
> Although known to be insecure, the Merkle-Hellman knapsack public-key encryption
> scheme is presented in §8.6 for historical reasons – it was the first concrete
> realization of a public-key encryption scheme. Chor-Rivest encryption is also
> presented (§8.6.2) as an example of an as-yet unbroken public-key encryption
> scheme based on the subset sum (knapsack) problem.

「已知不安全、為了歷史理由才收錄」——這是作者的話，不是我的判斷。
第一遍讀直接跳過 6 頁。

<!-- -->
> ⚠️ **§8.5 McEliece 有一個書上不可能知道的轉折**（不是書上的內容）：
> 它在 1996 年是冷門，但因為**不依賴分解或離散對數**，
> 今天成了後量子密碼的主要候選之一（Classic McEliece）。
> 第一遍仍然跳過——但知道這件事，日後聽到這個名字不會覺得陌生。

#### ⑤ ⚠️ 時代落差

> 📄 **原文**　書 p.290 ｜ PDF p.307
>
> 8.7 Note (recommended size of modulus) Given the latest progress in algorithms
> for factoring integers (§3.2), a 512-bit modulus n provides only marginal security
> from concerted attack. As of 1996, in order to foil the powerful quadratic sieve
> (§3.2.6) and number field sieve (§3.2.7) factoring algorithms, a modulus n of at
> least 768 bits is recommended. For long-term security, 1024-bit or larger moduli
> should be used.

⚠️ **這段的數字全部作廢**（不是書上的內容）：768-bit 已於 2009 年被實際分解，
1024-bit 早已不足；今天的下限是 **2048-bit**，長期用 **3072-bit 以上**。
**但推理方式沒有作廢**——「模數大小 ↔ 分解演算法的能力」這個掛鉤關係，
正是這一節要你學的東西。讀 Note 8.7 是為了學那個關係，不是為了記那些數字。

⚠️ 另外兩點，細節留給文末總表：這章沒有 **OAEP padding**（書上的是 textbook RSA，
直接拿來用是不安全的），也沒有 **ECC**（今天公鑰的主流）。

#### ⑥ 讀完應該答得出來的 3 個問題

1. 公鑰是 $(n, e)$、私鑰是 $d$——為什麼「知道 $n$ 和 $e$ 卻算不出 $d$」？
   這件事跟「分解 $n$」是**同一個問題**嗎？（§8.2.2(i) 與 Fact 8.6 講了，答案有陷阱）
2. 不看書，把 Example 8.4 的金鑰產生 → 加密 → 解密用紙筆重跑一次，
   每一步說得出在算什麼。
3. 為什麼實務上不用 RSA 直接加密整份檔案，而是用它來傳一把對稱金鑰？
   （§8.1 開頭那段自己講了理由）

📖 **書頁 283–320** ｜ PDF 頁 300–337 ｜ [開啟 PDF](./handbook-of-applied-cryptography.pdf#page=300)

---

## 本輪沒做什麼

按 [brief](./hac-reading-guide-brief.md) 的檢查點設計，下一輪補：

- **§2 其餘六站**（站 1、2、4、5、6、7）的完整六格
- **§3 數學前置反查索引** — 第 2、3 章的小節 → 被主線哪幾站用到
  （站 3 的「② 讀之前先補」是這張表的第一批資料）
- **§4「這本書哪些地方老了」總表** — 內文的 ⚠️ 一行標記在這裡集中展開
- **§5 書頁 ↔ PDF 頁換算表** — 複用 `crypto-course-notes-brief.md` 的

不做：HTML／PDF、習題解答、非主線章節的細部導讀。
