# 課程筆記 Brief — 密碼學（Cryptography）課程

- **來源**：課程錄影（線上授課，英語授課）
- **逐字稿**：
  - 第 1 堂前半 — `transcripts/lecture-01a-k8QFYlUURUs.en.txt`
    （<https://youtu.be/k8QFYlUURUs>）
  - 第 1 堂後半 — `transcripts/lecture-01b-z-M7QyqLQR4.en.txt`
    （<https://youtu.be/z-M7QyqLQR4>）
- **定案日期**：2026-08-30
- **階段**：第 1 章（第 1 堂課）尚未動筆，本 brief 為第一版規格。
- **對照書**：`handbook-of-applied-cryptography.pdf`（803 頁，見 §3 對照書目）
- **產出檔案**：`crypto-course-notes.md`（**一整份持續長大**，每堂課往下接）
- **最後修訂**：2026-08-30（第二次：加入課本對照機制）

---

## 1. Purpose

**給自己修這門課用的複習底稿。**

目標：期中期末考前不用重看影片，看這份就能把老師講過的**定義**、**例子**、
以及他點名的「**為什麼這樣不安全**」用自己的話講出來。

定位是「**考得出來**」，不是「**做得出來**」：

- 不寫程式實作。
- 但老師在課堂上算過的東西要能自己重算一遍
  （例如凱撒密碼怎麼加減、為什麼 26 把鑰匙用一個 for 迴圈就破了）。

**課務規定要記**（加分報告怎麼做、課本、考試方式、點名政策），
但**單獨放一節**，不要跟觀念混在一起。

## 2. Situation

### 來源品質很差，這是最大的坑

兩支影片都只有 **YouTube 自動字幕**，辨識錯誤很多。已知的例子：

| 字幕寫的 | 實際是 |
|---|---|
| `Addis` | Alice |
| `水鯊` / `water shark` | Wireshark |
| `PSI 頂點` | ciphertext（密文） |
| `亞洲加密` | **symmetric**（對稱）加密 |
| 老師口誤「金鑰可選 0 到 255」 | 凱撒密碼是 **0 到 25** |

> **原則：逐字稿只能當線索，不能當事實。**
> 寫進筆記的每個技術點都要用密碼學常識檢查過。
> 發現老師口誤或字幕出錯，**筆記寫正確的版本**，並加一個標記說明原稿是什麼。

**中文機器翻譯版不可用。** 一開始只抓到影片二的中文自動翻譯（9.9k 字），
後來抓到英文原稿是 32.6k 字 —— 翻譯版把內容砍掉約三分之二。
**只用英文原稿。**

### 其他背景

- **兩支影片是同一堂課的前後半**。影片一結尾老師喊休息「九點回來」，
  影片二從那之後接著講。合起來算「**第 1 章**」，不是兩章。
- **讀者（我）不是零基礎。** repo 裡已有 `linux-secure-boot-notes.md`，
  對稱／非對稱金鑰那些寫過了。不用從零解釋，可以直接連結過去。
- **考試是英文出題。**

### 語言

**筆記中文為主，專有名詞保留英文**（Confidentiality、ciphertext、
symmetric key、Wireshark…），因為考試是英文的。

## 3. Inputs

### 主要來源

1. `transcripts/lecture-01a-k8QFYlUURUs.en.txt` — 第 1 堂前半，英文原稿，16.9k 字
2. `transcripts/lecture-01b-z-M7QyqLQR4.en.txt` — 第 1 堂後半，英文原稿，32.6k 字

### 課本書目（由使用者提供，來自老師投影片）

1. Hans Delfs, Helmut Knebl, *Introduction to Cryptography: Principles and
   Applications* (2nd Ed.), Springer, 2007.
2. Alfred J. Menezes, Paul C. van Oorschot, Scott A. Vanstone,
   *Handbook of Applied Cryptography*, CRC Press, 2018.
3. William Stallings, *Network Security Essentials: Application and Standards*
   (4th Ed.), Pearson & Prentice Hall, 2010.

> ⚠️ **有一處對不上，兩邊都記，不自己選一個。**
> 老師口頭說「**第一本**」是他的最愛、不厚、作者放了免費 PDF、台灣買不到；
> 說「**第二本**」很厚、超過一千頁。
> 但實際上有免費官方 PDF 的是**第二本** Menezes 的 *Handbook of Applied
> Cryptography*（CRC Press 授權，滑鐵盧大學 CACR 站上一章一個 PDF：
> <https://cacr.uwaterloo.ca/hac/>）。Delfs & Knebl 與 Stallings 沒有免費版。
> 編號對不上 —— 可能是老師口述順序與投影片不同，也可能是字幕聽錯。
> **筆記照投影片名單寫，老師的口頭評語另標一行，開學可跟老師確認。**

### 對照書目：Handbook of Applied Cryptography

課程本身沒有指定課本頁碼，但這本有免費全文，**拿來當「老師講的東西書上在哪」的對照**。

- **檔案**：`handbook-of-applied-cryptography.pdf`（合併版，共 **803** 頁）
- **來源**：<https://cacr.uwaterloo.ca/hac/>（CRC Press 授權免費下載）
- 合併順序：目錄 → 第 1–15 章 → 附錄 → 參考文獻 → 索引

#### 標示方法（比照 `linux-secure-boot-notes.md`）

每個小節結尾放一行 **📖 對照**，格式：

```
📖 **對照** HAC §1.4 ｜ 書頁 15–16 ｜ PDF 頁 25–26 ｜ [開啟](./handbook-of-applied-cryptography.pdf#page=25)
```

- **書頁** = 印在紙上的頁碼；**PDF 頁** = 這個合併檔的第幾頁。**兩者差值不固定。**
- 再附**一句話**說明書上那段補了什麼老師沒講的（用自己的話寫）。
- 老師講的東西如果書上找不到對應，就**不放這行**，不要硬湊。

#### 書頁 → PDF 頁換算表

逐頁核對頁首/頁尾印出的頁碼後得到：

| 書頁 | PDF 頁 | 加多少 |
|---|---|---|
| 1–48 | 11–58 | +10 |
| 49–86 | 60–97 | +11 |
| 87–132 | 99–144 | +12 |
| 133–168 | 146–181 | +13 |
| 169–190 | 183–204 | +14 |
| 191–222 | 206–237 | +15 |
| 223–282 | 239–298 | +16 |
| 283–424 | 300–441 | +17 |
| 425–488 | 443–506 | +18 |
| 489–590 | 508–609 | +19 |
| 591–634 | 611–654 | +20 |
| 635–702 | 656–723 | +21 |
| 703–754 | 725–776 | +22 |
| 755–780 | 778–803 | +23 |

#### 各章頁碼對照（已逐章核對章名頁）

| 章 | 標題 | 書頁起 | PDF 頁 |
|---|---|---|---|
| 1 | Overview of Cryptography | 1 | 11–59 |
| 2 | Mathematical Background | 49 | 60–98 |
| 3 | Number-Theoretic Reference Problems | 87 | 99–145 |
| 4 | Public-Key Parameters | 133 | 146–182 |
| 5 | Pseudorandom Bits and Sequences | 169 | 183–205 |
| 6 | Stream Ciphers | 191 | 206–238 |
| 7 | Block Ciphers | 223 | 239–299 |
| 8 | Public-Key Encryption | 283 | 300–337 |
| 9 | Hash Functions and Data Integrity | 321 | 338–401 |
| 10 | Identification and Entity Authentication | 385 | 402–442 |
| 11 | Digital Signatures | 425 | 443–507 |
| 12 | Key Establishment Protocols | 489 | 508–561 |
| 13 | Key Management Techniques | 543 | 562–610 |
| 14 | Efficient Implementation | 591 | 611–655 |
| 15 | Patents and Standards | 635 | 656–683 |
| 附錄 A | Bibliography of Papers from Selected Cryptographic Forums | — | 684–724 |
| — | References | — | 725–777 |
| — | Index | — | 778–803 |

> ⚠️ **取頁碼時注意**：每章的**章名頁沒有頁首**，頁首從該章第二頁才出現。
> 用頁首自動抓章節起始頁會**整章少一頁**。上表已修正，取的是章名頁。

### 次要來源

我自己的密碼學常識，**只**用在兩件事：

- 修正字幕辨識錯誤 / 老師口誤
- 補一句白話解釋

凡是這種地方，筆記裡要標出來（比照 `linux-secure-boot-notes.md` 的
`⚠️ 本節不是書上的內容` 寫法）。

### 禁止

- 老師的投影片我們**沒有**，不要憑空補投影片上的內容。
- 查不到的**留白**，不要生一個看起來很合理的答案填進去。

## 4. Limits

- **不逐字抄逐字稿。** 用自己的話重寫。要引用老師原話時只引一兩句，
  標清楚是引用。
- **不寫進度外的內容。** 這堂只講到「CIA 三目標」與「對稱 vs 公鑰」。
  RSA 數學、AES 內部結構、hash function 一律不碰 —— 那是後面的課，
  先寫會跟老師的順序打架。
- **不寫實作。** 不放程式碼，不放 Wireshark 操作步驟。
  老師提 Wireshark 只是舉例說明「偷看很容易」。
- **不改老師的架構。** 他怎麼分（目標 → 對稱 → 凱撒 → 破解手法 → 公鑰），
  筆記就怎麼排。考試照他的講法出。
- **不動現有檔案。** `linux-secure-boot-notes.md` 與其 brief 完全不碰，
  最多在新筆記裡放連結過去。
- **這輪不做 html / pdf。** 先把 md 寫對，之後再決定要不要跑
  `tools/build_notes_html.py`。
- **不整段引用課本。** 對照書只放**頁碼指標**加一句自己寫的說明，
  不把 HAC 的段落抄進筆記。（這點與 `linux-secure-boot-notes.md` 不同 ——
  那份是自己買的書、逐節附原文；HAC 是公開授權的免費書，
  指標式引用就夠用，也避免筆記變成抄書。）
- **對照不到就不放。** 硬把老師的話塞進書上某一節，比留白更糟。
- **遇到對不上的資訊，兩邊都記，不自己選一個。**

## 5. Done-when

### 檢查點（先做這個）

先產出 **brief（本檔）** + **只有標題和一句話說明的骨架**，
給使用者看過點頭，**才**填內容。

### 完成的樣子（本輪）

- `crypto-course-notes-brief.md` — 本規格檔
- `crypto-course-notes.md` — 筆記本體，**只寫第 1 章：課程總覽與密碼學的目標**
- 每個小節結尾標**來源影片**（影片一 / 影片二）—— **不標時間戳**
- 對得上的小節再加一行 **📖 對照**：HAC 章節 ｜ 書頁 ｜ PDF 頁 ｜ 可點連結
  ＋ 一句話說明書上補了什麼
- 一節「**課務規定**」：加分報告、課本、考試方式、點名政策
- 一節「**本堂名詞小抄**」：中英對照
- 結尾一段「**這堂課的重點三句話**」，考前掃一眼用

### 不做

html、pdf、第 2 堂以後的內容。
