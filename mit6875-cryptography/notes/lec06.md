# Lecture 6 — One-Way Functions, Hardcore Bits, Goldreich–Levin

> **來源說明**
> - 投影片：`slides/lec06.pdf`（**Fall 2022**，33 頁，有完整文字層）—— **主要來源**。
> - 影片：這堂的材料**散在 2018 那套的四支影片裡**。三支的 YouTube 字幕是舊版（沒標點、漏字嚴重），我都自行用 Whisper 重轉了。
>
> | lec06 投影片 | 影片來源 | 字幕 |
> |---|---|---|
> | p2–7 OWF 定義 | **L2** `7YfYYIvyYb8` `[43:40]`–`[52:49]` | 🔧 自轉 |
> | p9–15 Hardcore bits | **L4**「Hardcore Bits」`H008GInK0xc` `[43:40]`–`[48:16]` | 🔧 自轉 |
> | p17–21 OWP ⇒ PRG | **L6** `fdr6RKyjhEs` `[72:39]`– | YouTube（品質好） |
> | p23–32 Goldreich–Levin | **L5**「Hardcore Bits II」`UuQuF0tcn1E` | 🔧 自轉 |
>
> **自轉是必要的，不是多此一舉。** 以 L4 為例：
>
> | | YouTube 字幕 | 自轉 Whisper |
> |---|---|---|
> | 總字數 | 8890 | **12463** |
> | "hardcore" | 3 | **20** |
> | "one-way" | 7 | **25** |
>
> YouTube 那份**漏掉了近三成內容**。（相對地 L6 拿到的是新版字幕，自轉沒有加值 —— 判斷標準見 `BRIEF.md`。）
>
> ⚠️ Whisper 仍會聽錯人名：**Goldreich–Levin 被聽成 “Goldrack”、Chernoff 被聽成 “Chernobyl”**。數學內容一律以投影片為準。
>
> **不寫進本筆記的部分**：L4 後半整段是「用 discrete log 證明最高位元是 hardcore」，那是 Fall 2022 的 **lec07**（Goldreich–Levin contd.、discrete log）。
>
> 標 `📎 補充` 的區塊不是課堂內容，是我額外加的。

---

## 一句話總結

**One-way function 是整座密碼學大樓的地基** —— 而 Goldreich–Levin 定理說：**每一個 OWF 都自帶一個「難猜的位元」**，於是從 OWF 就能一路造出 PRG、PRF、加密⋯⋯整個 Minicrypt。

---

## 這週要做四件事（p3）

1. 定義 **one-way functions (OWF)**
2. 定義 **hardcore bits (HCB)**
3. 證明 **one-way permutations (OWP) ⇒ PRG**
4. **Goldreich–Levin 定理**：每個 OWF 都有一個 HCB

---

## 0. 課程地圖：兩個 Crypto 世界

（投影片 p2）

投影片畫了一張整門課的地圖，把密碼學原語分成兩層：

**Minicrypt**（lecture 2–7、11–12）—— 地基是 **OWF**：

```
                              OWF
                    ╱      ╱   │   ╲       ╲
             Hashing      │  PRG    │    Digital
                          │   │     │    Signatures
                   Bit    │  PRF    │
              Commitment  │   │     │
                          │  Secret-key encryption
                          │  (Stateful → Stateless)
                          │   │
                          │  MAC → CCA-secure secret-key enc.
```

**Cryptomania**（lecture 8–10⋯）—— 需要更強的假設：

- Public-key encryption
- Zero-knowledge proofs

> 💡 **前五堂課學的每一樣東西，最終都掛在 OWF 這一個假設上。** 這堂就是去看那個地基本身。

---

## 1. One-Way Functions

### 非正式（p4）

一個函數 $F$，**容易計算、難以反轉**。

```
   domain  ──────── F ────────▶  range
            易於計算 →
            ← 難以反轉
```

### Take 1：第一次嘗試（p5）

函數族 $\{F_n\}_{n \in \mathbb{N}}$，其中 $F_n : \{0,1\}^n \to \{0,1\}^{m(n)}$，稱為 **one-way**，若對每個 p.p.t. 對手 $A$，存在 negligible $\mu$：

$$\Pr\big[x \leftarrow \{0,1\}^n;\, y = F_n(x) \;:\; A(1^n, y) = x\big] \;\le\; \mu(n)$$

**這個定義壞掉了。**

**反例**：取 $F_n(x) = 0$（對所有 $x$ 都輸出 0）。

這個函數**符合上面的定義** —— 事實上，**即使 $A$ 有無限時間也不可能找到那個 $x$**，因為 $y = 0$ 完全不帶 $x$ 的資訊。

> **結論：這不是一個有用／有意義的定義。**

**問題出在哪**：定義要求還原出**原本那個** $x$。但那可能**資訊理論上就不可能**，跟「計算困難」無關。我們要的是計算困難，不是資訊不足。

### 正確的定義（p6–p7）

> **The Right Definition: Impossible to find an inverse in p.p.t.**

$$\Pr\Big[x \leftarrow \{0,1\}^n;\, y = F_n(x);\, A(1^n, y) = x' \;:\; y = F_n(x')\Big] \;\le\; \mu(n)$$

**關鍵改動**：$A$ 只要找到**任何一個** $x'$ 滿足 $F_n(x') = y$ 就算成功 —— 不必是原本那個 $x$。

這樣一來 $F_n(x) = 0$ 就不再是 OWF 了（隨便給一個 $x'$ 都行）。

投影片並列的兩句話把意思說完了：

> - 用**無限時間**永遠找得到反像
> - ⋯⋯但用 **p.p.t.** 應該很難

**影片裡的說法（L2 [45:45]）**：如果給你指數時間，你就**把所有的 $x$ 試一遍**，直到找到 $F(x) = y$ 為止。所以困難性**只能**是計算上的。

### One-Way Permutations (OWP)（p7）

> **一對一**的 one-way function，且 $m(n) = n$。

也就是定義域和值域一樣大、而且是雙射。**每個 $y$ 恰好有一個反像。**

### 「我們不知道它存不存在」（L2 [44:23]）

這是課堂上講得很重、投影片沒寫的一段：

> 從這裡開始，**幾乎所有東西都依賴 one-way function 的存在。而我們不知道怎麼證明它存在。**
> 我們只有**候選**。你在網路上看到的所有密碼學，都建立在「這些候選真的是 OWF」這件事上。
>
> 「這件事不是每堂密碼學課都會講，但它們應該講。」

> 💡 **這跟 lec02 那句「若 $P = NP$ 則 PRG 不存在」是同一件事的兩面。** OWF 存在蘊含 $P \ne NP$，
> 所以證明 OWF 存在**至少**和解決 $P$ vs $NP$ 一樣難。

### 第一個候選：乘法（L2 [50:41]–[52:49]）

$$F(p, q) = p \cdot q$$

- **正向容易**：小學就學過乘法。
- **反向是 factoring**：給你 $N = p \cdot q$，找出 $p$ 和 $q$。

課堂上給了目前最好演算法的執行時間（**general number field sieve**），大約是

$$e^{\,c \,(\log N)^{1/3} (\log\log N)^{2/3}}$$

**sub-exponential（次指數）** —— 比任何多項式慢，但比純指數快。

**但 Vinod 立刻把這個候選否定掉了：**

> 等等，我們做完了嗎？**沒有。這其實不是個好候選。**
>
> 因為定義要求**每一個**反轉者都必須失敗 —— 除了極小一部分的輸入之外，它得**一直**失敗。

> 📎 **為什麼乘法不合格**：隨便抽兩個數相乘，$N$ **有 3/4 的機率是偶數**（只要 $p$ 或 $q$ 任一為偶）。
> 偶數一眼就能分解出因數 2。所以「隨機輸入」上的反轉成功率遠遠不是 negligible。
>
> **修法**：把定義域限制成**質數**（或大質數對）。這就是為什麼 RSA 用的是兩個大質數的乘積，
> 而不是隨便兩個數。細節在 lec09。

---

## 2. Hardcore Bits

### 動機（p9）

OWF 保證「算出**整個**反像很難」。但是：

> **關於反像的「部分資訊」呢？**

> **Exercise：存在一些 one-way function，它的反像的「前一半位元」是容易算出來的。**

> 📎 **這個練習的構造很簡單**：若 $F$ 是 OWF，定義 $F'(x_1 \| x_2) = x_1 \| F(x_2)$。
> $F'$ 仍然是 OWF（要反轉它還是得反轉 $F$），但它**把前一半明文照抄輸出**。

**所以「$F$ 是 OWF」完全不保證「$F(x)$ 藏住了 $x$ 的每個位元」。** 這是個問題 —— lec02 的 PRG 需要的是「看起來隨機」，不是「整個算不出來」。

### Take 1：某一個位元（p10–p11）

**想法**：既然整個 $x$ 難算，總該有**某一個位元**是難的吧？

先要把「難算」翻譯成對的話：

> - **任何一個位元，亂猜就有 $1/2$ 的機率猜中。**
> - 所以「難以計算」要改成 **「難以用顯著優於 $1/2$ 的機率猜中」**。

> **HARDCORE BIT (Take 1).** 對函數族 $F: \{0,1\}^n \to \{0,1\}^m$，位元 $i = i(n)$ 是 **hardcore** 的，
> 若對每個 p.p.t. 對手 $A$，存在 negligible $\mu$：
> $$\Pr\big[x \leftarrow \{0,1\}^n;\, y = F(x) \;:\; A(y) = x_i\big] \;\le\; \frac{1}{2} + \mu(n)$$

### 為什麼 Take 1 也不夠（p12）

> **PS2：存在一些函數，它是 one-way 的，但它的**每一個**位元都「有點容易」猜（比方說用機率 $\frac12 + \frac1n$）。**

$\frac12 + \frac1n$ 不是 negligible 的優勢，所以**沒有任何一個位元是 hardcore 的** —— 但這個函數仍然是 OWF。

> **所以我們要把 hardcore「位元」的概念一般化。**

### Hardcore Predicate（p13）

**關鍵一步：不要指定 $x$ 的某一個位元，改成允許任何「輸出一個位元的函數」。**

> **HARDCORE PREDICATE (Definition).** 對函數族 $F: \{0,1\}^n \to \{0,1\}^m$，
> 一個函數 $B: \{0,1\}^n \to \{0,1\}$ 是 **hardcore predicate**，
> 若對每個 p.p.t. 對手 $A$，存在 negligible $\mu$：
> $$\Pr\big[x \leftarrow \{0,1\}^n;\, y = F(x) \;:\; A(y) = B(x)\big] \;\le\; \frac{1}{2} + \mu(n)$$

> 此後我們說 hardcore bit，都是指 hardcore predicate。

### 圖像（p14）

```
              易於計算
        x ─────────────▶ F(x)
        │                 │
        │ 易於計算        │ 難以計算
        ▼                 ╱
       B(x) ◀────────────╱
```

$B(x)$ **從 $x$ 很容易算**，但**從 $F(x)$ 幾乎不可能猜**。

**課堂上的措辭（L4 [44:13]–[44:43]）**：

> predicate 就是**輸出一個位元的函數**，如此而已。
> $B$ 給定 $x$ 很容易算（$B$ 是多項式時間可計算的），但**只給 $F(x)$ 就非常非常難算**。
>
> 而且「難算」還不夠。我要的是 **「難以顯著優於亂猜地預測」**。

### 對定義的三點討論（p15）

1. **HCP 的定義對任何函數族都說得通**，不限於 one-way function。
2. **有些函數的 predicate 是資訊理論上難猜的**（例如壓縮型的函數 —— 資訊根本不在那裡）。
3. **我們感興趣的是這個情形**：$F(x)$ **唯一決定**了 $x$，**然而** $B(x)$ 仍然難以預測。

> 💡 第 3 點是整個概念的精髓，也是它「反直覺」的地方：
> **$F(x)$ 裡明明完整包含了 $x$ 的資訊**（想想 one-way permutation —— 反像唯一），
> **但那個資訊在計算上取不出來。**
> 這正是 lec02「計算安全 ≠ 資訊理論安全」的最尖銳體現。

### 已知的例子（L4 [46:42]）

課堂上提到，**個別的**one-way function 往往有很自然的 hardcore predicate：

| 函數 | Hardcore predicate |
|---|---|
| Discrete log | **最高位元**（要適當定義，見下） |
| RSA | **最低位元**（據說其實**每個**位元都是 hardcore 的） |

⚠️ 但這帶出一個麻煩：

> 每次有人提出一個新的 one-way function，難道你都要**盯著它看**、猜哪個位元是 hardcore
> （有時是最高位元、有時是最低位元、有時是 parity、有時都不是⋯⋯誰知道？），**然後從頭證一次**？

**答案是不用。** 那就是第 4 節的 Goldreich–Levin 定理。

> 📎 **一個學生問的好問題（L4 [48:16]）**：那 MD5 之類的雜湊函數呢，它有 hardcore bit 嗎？
> Vinod 的回答：**沒有人證明過 MD5 的任何單一位元是 hardcore 的。** 你可以「宣稱」，但那不算數 —— 這些事情需要證明。他說這是個有趣的開放問題。

> ⚠️ 「discrete log 的最高位元是 hardcore」這件事的**證明**（以及「天真定義的最高位元其實有偏、根本不是 hardcore」這個陷阱）佔了 L4 後半整堂，屬於 **lec07**，本筆記不寫。

---

## 3. OWP ⇒ PRG

（投影片 p17–21）

### 建構

設 $F$ 是 one-way **permutation**，$B$ 是 $F$ 的一個 hardcore predicate。定義：

$$\boxed{\;G(x) \;=\; F(x) \,\|\, B(x)\;}$$

> **Theorem：假設 $F$ 是 one-way permutation，則 $G$ 是 PRG。**

$G$ 把 $n$ bits 拉長成 $n+1$ bits。**而 lec03 已經教過怎麼把「拉長一個 bit」變成「拉長多項式個 bit」。**

> 💡 **這就是 lec02 那張依賴圖上「OWF → PRG」那條線。** 拼圖在這裡合起來了。

### 證明：用 next-bit unpredictability

（又一次靠 lec03 那個等價定理 —— 直接證 indistinguishability 很麻煩，證 NBU 容易。）

**反證。** 假設 $G$ 不是 PRG。則存在 next-bit predictor $D$、下標 $i$、多項式 $p$：

$$\Pr\big[x \leftarrow \{0,1\}^n;\, y = G(x) \;:\; D(y_1 \dots y_{i-1}) = y_i\big] \;\ge\; \frac{1}{2} + \frac{1}{p(n)}$$

**Observation（p19）：$i$ 一定是 $n+1$。看得出為什麼嗎？**

> **Hint：$G(x) = F(x) \| B(x)$，而 $F$ 是 one-way permutation。**

> 📎 **答案**：輸出的前 $n$ 個位元就是 $F(x)$。因為 $F$ 是**排列**而 $x$ 是均勻隨機的，
> **$F(x)$ 本身就是均勻隨機的** —— 它的任何一個位元都無法從前面的位元預測（機率恰好 $1/2$）。
> 所以唯一可能被預測的位置，只剩最後那一個：$y_{n+1} = B(x)$。

於是那個式子變成

$$\Pr\big[x \leftarrow \{0,1\}^n \;:\; D(y_1 \dots y_n) = y_{n+1}\big] \;=\; \Pr\big[x \leftarrow \{0,1\}^n \;:\; D(F(x)) = B(x)\big] \;\ge\; \frac{1}{2} + \frac{1}{p(n)}$$

> **所以 $D$ 就是一個 hardcore bit 的預測器！QED.**

**證明就這麼短。** 因為「$G$ 的最後一個位元不可預測」和「$B$ 是 hardcore」根本是同一句話。

**課堂上的總結（L6 [72:39]）**：

> 拿任何一個 one-way permutation，配上它的任一個 hardcore bit，**你就成了**。
> 例如 discrete log + 最高位元，或者任何 one-way permutation + Goldreich–Levin 的 hardcore bit。**都行。**
>
> 這是從任何 one-way permutation 得到 PRG 的**通用配方**。

---

## 4. Goldreich–Levin 定理

（投影片 p23–32）

### 先問一個更貪心的問題（p23）

> 我們來追求一個 **universal hardcore predicate** —— **單一一個** predicate $B$，
> 使得對**任何** OWF $F$，給定 $F(x)$ 都難以猜出 $B(x)$。
>
> 做得到嗎？**答案是「不行」。你會在 PS2 告訴我為什麼。**

> 📎 **直覺**：固定了 $B$ 之後，敵人可以**針對 $B$ 去設計** $F$ —— 例如讓 $F(x)$ 直接把 $B(x)$ 抄在輸出裡。
> 這個 $F$ 仍然可以是 OWF，但 $B$ 對它顯然不 hardcore。

**那怎麼辦？**

### GL 定理（p24–25）

**答案：不要用單一一個 predicate，用一整族，然後隨機挑一個。**

定義一族 predicate $\{B_r : \{0,1\}^n \to \{0,1\}\}$，每個 $r$ 一個：

$$B_r(x) \;=\; \langle r, x \rangle \;=\; \sum_{i=1}^{n} r_i x_i \bmod 2$$

（也就是 $r$ 和 $x$ 的**內積 mod 2** —— 等價於「把 $r$ 指定的那些位元 XOR 起來」。）

> **THEOREM (Goldreich–Levin).** 隨機挑的 $B_r$ 對**每一個** one-way function $F$ 都是 hardcore 的。
> 也就是說，對每個 OWF $F$、每個 PPT $A$，存在 negligible $\mu$：
> $$\Pr\big[x \leftarrow \{0,1\}^n;\, r \leftarrow \{0,1\}^n \;:\; A(F(x), r) = B_r(x)\big] \;\le\; \frac{1}{2} + \mu(n)$$

**注意 $r$ 也是隨機的、而且會交給對手。** 這正好繞過上面那個「敵人針對 $B$ 設計 $F$」的問題 —— **$F$ 必須在看到 $r$ 之前就被設計好。**

### 兩種等價的說法

**詮釋 1（p24）**：對每個 OWF $F$，存在一個相關的 OWF

$$F'(x, r) = \big(F(x),\, r\big)$$

它有一個**確定性的** hardcore predicate。

（把隨機性 $r$ 吸收進函數的輸入裡。這是實務上用的形式 —— 第 3 節的 OWP ⇒ PRG 就可以直接套用。）

**詮釋 2（p25）**：對每個 OWF $F$，**非均勻地（non-uniformly）**存在一個 hardcore predicate $\langle \hat{r}, x \rangle$。

> 投影片作者加了一句：**「我最喜歡的開放問題：把這個 non-uniformity 拿掉。」**

---

### 證明（p26–30）

**目標**：假設有一個能猜 $\langle r, x\rangle$ 的 predictor $P$，用它造出 $F$ 的**反轉器** $A$。

$$\Pr\big[x \leftarrow \{0,1\}^n \;:\; A(F(x)) = x' \;\wedge\; F(x') = F(x)\big] \;\ge\; \frac{1}{p'(n)}$$

證明分三個難度遞增的版本。

---

#### 版本 A：完美的 predictor（p27）

先把日子過簡單一點：假設 $P$ **永遠正確**。

$$\Pr\big[x, r \;:\; P(F(x), r) = \langle r, x \rangle\big] = 1$$

**反轉器 $A$**：輸入 $y = F(x)$，把 $P$ 跑 $n$ 次，輸入分別是

$$(y, e_1),\; (y, e_2),\; \dots,\; (y, e_n)$$

其中 $e_i$ 是**單位向量**（$e_1 = 100\cdots0$、$e_2 = 010\cdots0$⋯）。

因為 $\langle e_i, x \rangle = x_i$，第 $i$ 次呼叫就直接吐出 $x$ 的第 $i$ 個位元。

**$n$ 次呼叫，拼出整個 $x$。** 完成。

#### 為什麼這個做法撐不住（L5 [19:51]）

課堂上立刻指出問題：

> 這**只對完美的 predictor 有效**。
> 一個不完美的 predictor **大可以對這 $n$ 個特定的 $r$ 通通拒答**。
> 他只對**隨機的 $r$** 回答。
>
> 他完全可以對任何**固定的** $n$ 個 $r$ 說「不知道」，而仍然保有 non-negligible 的優勢 ——
> 因為 $n$ 相對於 $2^n$ 是極小的一撮。

**所以我們不能問 $P$ 我們想問的 $r$，只能問隨機的 $r$。** 這就是接下來所有技巧的來源。

---

#### 版本 B：夠好的 predictor（p28–30）

現在假設

$$\Pr\big[x, r \;:\; P(F(x), r) = \langle r, x \rangle\big] \;\ge\; \frac{3}{4} + \frac{1}{p(n)}$$

**第一步：averaging argument（p28）**

> **Claim：至少有 $\frac{1}{2p(n)}$ 比例的 $x$ 滿足**
> $$\Pr_{r \leftarrow \{0,1\}^n}\big[P(F(x), r) = \langle r, x \rangle\big] \;\ge\; \frac{3}{4} + \frac{1}{2p(n)}$$
>
> **Proof: Exercise in counting.**

把這些 $x$ 叫做 **good $x$**。（整體的平均優勢，必須有相當一部分來自「某些特別好的 $x$」。）

**第二步：關鍵想法 —— 線性（p29）**

我們不能問 $e_i$，但我們可以**問兩個隨機的 $r$，讓它們的差是 $e_i$**：

$$\langle r, x \rangle \;\oplus\; \langle r \oplus e_i, x \rangle \;=\; \langle e_i, x \rangle \;=\; x_i$$

這就是內積的**線性**。**課堂上稱它是 “the deep identity”（L5 [20:25]）** —— 語帶戲謔，但它確實是整個證明的支點。

**做法**：挑一個隨機的 $r$，向 $P$ 要 $\langle r, x\rangle$ 和 $\langle r \oplus e_i, x\rangle$，**把兩個答案 XOR 起來，得到 $x_i$**。

注意 $r$ 和 $r \oplus e_i$ **各自都是均勻隨機的**，所以 $P$ 沒辦法耍賴。

**成功率分析（用 union bound）**：

$$
\begin{aligned}
\Pr[\text{算對 } x_i]
&\ge \Pr[P \text{ 兩個都答對}] \\
&= 1 - \Pr[P \text{ 至少答錯一個}] \\
&\ge 1 - \Big(\Pr[\text{第一個錯}] + \Pr[\text{第二個錯}]\Big) && \text{(union bound)} \\
&\ge 1 - 2\left[\frac{1}{4} - \frac{1}{2p(n)}\right] \\
&= \frac{1}{2} + \frac{1}{p(n)}
\end{aligned}
$$

**第三步：放大成功率（p30）**

單次只有 $\frac12 + \frac{1}{p(n)}$，不夠 —— 我們要**每一個**位元都對。所以重複取多數決：

```
反轉器 A：
  對每個 i ∈ {1, 2, …, n}：
      重複 log n · p(n) 次：
          挑一個隨機的 r
          向 P 要 ⟨r, x⟩ 和 ⟨r ⊕ eᵢ, x⟩
          兩個 XOR 起來，得到 xᵢ 的一個猜測
      對所有猜測取「多數決」，定下 xᵢ
  輸出所有 xᵢ 串起來的 x
```

**分析：Chernoff bound + union bound。**
（Chernoff 保證每個位元的多數決以極高機率正確；union bound 保證 $n$ 個位元**同時**都對。）

---

#### 版本 C：真正的證明（p31，下一講）

實際的定理只假設

$$\Pr_r\big[P(F(x), r) = \langle r, x \rangle\big] \;\ge\; \frac{1}{2} + \frac{1}{2p(n)}$$

**注意是 $\frac12$，不是 $\frac34$。** 這差很多 —— 版本 B 的 union bound 直接垮掉（$1 - 2 \cdot \frac12 = 0$，什麼也保證不了）。

> **Key Idea：Pairwise independence（兩兩獨立）**
>
> 參考：Goldreich 的書 Part 1, Section 2.5.2

**課堂上講的思路（L5 [45:22]–[51:30]）**，這段很精彩：

**問題出在哪**：我們需要知道 $\langle r, x\rangle$ 的正確值，但 $P$ 只有 51% 的把握。

**一個「作弊」的想法**：那就**不要問 $P$，自己猜** $\langle r, x\rangle$！
如果我們**條件在「所有猜測都對」**這個事件上，那 $\frac14$ 的誤差就消失了，剩下的機率變回 $\frac12 + \frac{1}{p(n)}$，多數決又能用了。

**但這是作弊**：猜對所有 $r$ 的內積，機率低到跟直接猜 $x$ 一樣荒謬。

**破解**：

> **整個分析我從來不需要這些 $r$ 是「完全隨機」的 —— 我只需要它們「兩兩獨立」。**

於是策略變成：

1. **只挑 $\log m$ 個真正隨機的種子** $s_1, s_2, \dots, s_{\log m}$。
2. **猜** $\langle s_1, x\rangle, \dots, \langle s_{\log m}, x\rangle$ —— 只有 $\log m$ 個位元要猜。
   猜對的機率是 $2^{-\log m} = \frac1m$ —— **而且你甚至可以把 $2^{\log m} = m$ 種可能全部枚舉一遍**，
   反正 $m$ 是多項式。
3. **把這 $\log m$ 個種子展開成多項式多個兩兩獨立的 $r$**：
   每個 $r$ 由一個**子集合** $T \subseteq \{1, \dots, \log m\}$ 索引，取對應種子的 XOR。
   而且 $\langle r_T, x \rangle$ 也就等於那些 $\langle s_i, x\rangle$ 的 XOR —— **所以猜了種子就等於知道了全部。**
4. 因為只有兩兩獨立，集中不等式從 **Chernoff 換成 Chebyshev**，需要的樣本數從 $\log n$ 變成大約 $p(n)^2$。

課堂上對第 4 點的評語：

> 那又怎樣呢？$p(n)^2$ 和 $p(n)^2 \cdot n^2$ 之間有差嗎？**一個多項式跟另一個多項式，都一樣。**

> 💡 Vinod 說這是 **pairwise independence 在理論計算機科學裡最早的用途之一**。
> 核心是一個很省的觀念：**真隨機很貴，但很多證明其實只需要「兩兩獨立」，而那個可以從對數個種子便宜地造出來。**
> （這跟 lec02「真隨機是稀缺資源」是同一個精神。）

---

### 編碼理論的視角（p32）

**這一頁把整個證明重新詮釋了一次，非常值得看。**

把映射

$$x \;\longmapsto\; \big(\langle x, r\rangle\big)_{r \in \{0,1\}^n}$$

看成 $x$ 的一個編碼：它把 $n$ 個位元變成 $2^n$ 個位元，**極度冗餘、指數長**。

> **這就是 Hadamard code（阿達馬碼）。**

而 $P(F(x), \cdot)$ 可以想成：**提供一個「有雜訊的碼字」的存取管道** —— 你問某個位置，它回答，但有時候是錯的。

於是：

| | 相當於 |
|---|---|
| **我們證的（版本 B）** | Hadamard code 的 **unique decoding**（唯一解碼）演算法，容錯率 $\frac14 - \frac{1}{p(n)}$ |
| **真正的證明（版本 C）** | Hadamard code 的 **list-decoding**（列表解碼）演算法，容錯率 $\frac12 - \frac{1}{p(n)}$ |

> 💡 **為什麼 $\frac12$ 一定要用 list decoding**：雜訊率接近 $\frac12$ 時，**唯一解碼在資訊理論上就不可能** ——
> 可能有好幾個碼字都同樣接近你手上這串雜訊。
> 所以演算法只能吐出一個**候選清單**，再用 $F$ 去逐一驗證哪個才是對的（$F$ 容易計算，驗證很便宜）。
>
> 這也解釋了詮釋 2 的 **non-uniformity** 是從哪來的。

---

## Recap（p33）

1. 定義了 **one-way functions (OWF)**
2. 定義了 **hardcore bits (HCB)**
3. **Goldreich–Levin 定理**：每個 OWF 都有一個 HCB（本堂證了一個重要的特例）
4. 證明了 **one-way permutations ⇒ PRG**

> 投影片最後的補充：
> **事實上 one-way functions ⇒ PRG 也成立，但那是一個困難得多的定理。**

> 📎 那個定理是 **Håstad–Impagliazzo–Levin–Luby (HILL)**，證明極其複雜。
> 它的意義是：**Minicrypt 裡的所有東西，真的都只需要 OWF。**
> 本堂證的 OWP ⇒ PRG 是那個結果的簡單版本（多假設了「排列」這個條件）。

---

## 名詞對照表

| 英文 | 中文 | 說明 |
|---|---|---|
| one-way function (OWF) | 單向函數 | 易算難反轉 |
| one-way permutation (OWP) | 單向排列 | 一對一的 OWF，$m(n) = n$ |
| invert | 反轉 | 從 $F(x)$ 找出某個反像 |
| pre-image | 反像 | 滿足 $F(x') = y$ 的 $x'$ |
| Minicrypt | — | 只需要 OWF 的世界 |
| Cryptomania | — | 需要更強假設的世界（公鑰加密等） |
| hardcore bit / predicate | 硬核位元 / 硬核謂詞 | 從 $F(x)$ 難猜的那一個位元 |
| predicate | 謂詞 | 輸出單一位元的函數 |
| Goldreich–Levin theorem | — | 每個 OWF 都有 hardcore bit |
| inner product mod 2 | 模 2 內積 | $\langle r,x\rangle = \sum r_i x_i \bmod 2$ |
| unit vector $e_i$ | 單位向量 | 第 $i$ 位是 1、其餘為 0 |
| linearity | 線性 | $\langle r,x\rangle \oplus \langle r \oplus e_i, x\rangle = x_i$ |
| averaging argument | 平均論證 | 從整體優勢推出「有一批好的 $x$」 |
| union bound | 聯集界 | $\Pr[A \cup B] \le \Pr[A] + \Pr[B]$ |
| majority | 多數決 | 重複取樣後投票 |
| Chernoff bound | — | 獨立取樣的集中不等式 |
| Chebyshev | 柴比雪夫不等式 | 只需兩兩獨立的集中不等式 |
| pairwise independence | 兩兩獨立 | 任兩個獨立，但三個以上未必 |
| non-uniform | 非均勻 | 允許對每個 $n$ 有不同的「建議」 |
| Hadamard code | 阿達馬碼 | $n$ bits → $2^n$ bits 的極冗餘編碼 |
| unique decoding | 唯一解碼 | 雜訊率 $< 1/4$ 時可行 |
| list decoding | 列表解碼 | 雜訊率接近 $1/2$ 時，吐出候選清單 |
| general number field sieve | 一般數域篩法 | 目前最好的分解演算法 |

---

## 📎 外部補充（非課堂內容）

> 以下不在投影片、也不在四支影片裡，是我額外加的。

**1. OWF 存在 ⟹ $P \ne NP$**
「給定 $y$，是否存在 $x$ 使 $F(x) = y$ 且 $x$ 的第一個位元是 1」這類問題落在 NP 裡。若 $P = NP$，就能多項式時間逐位元問出一個反像。所以**證明 OWF 存在，至少和分開 $P$ 與 $NP$ 一樣難** —— 這就是課堂上那句「我們不知道怎麼證明」的精確版本。

**2. 為什麼 GL 用內積，而不是別的**
內積 $\langle r, x\rangle$ 的關鍵性質有兩個：**線性**（讓 $e_i$ 的技巧成立），以及**對固定的 $x \ne 0$，隨機 $r$ 下它是均勻的一個位元**（所以「$\frac12$」是對的基準線）。這兩個性質合起來，恰好就是 Hadamard code 的性質。

**3. 兩兩獨立怎麼從對數個種子造出來**
取 $\log m$ 個真隨機種子 $s_1, \dots, s_{\log m}$，對每個非空子集 $T$ 定義 $r_T = \bigoplus_{i \in T} s_i$。可以驗證：任兩個不同的 $r_T, r_{T'}$ 是均勻且獨立的，但三個就不是（例如 $r_{\{1\}} \oplus r_{\{2\}} \oplus r_{\{1,2\}} = 0$）。**這是 pairwise independence 的標準建構。**

**4. 延伸閱讀**
- Goldreich, *Foundations of Cryptography* Vol. 1，2.2 節（OWF）、2.5 節（hardcore predicates，含 GL 的完整證明）
- Katz–Lindell，7.1 節（OWF）、7.2 節（hardcore bits）、7.4 節（OWP ⇒ PRG）
- Boneh–Shoup（在 `books/`），第 3 章
- 原始論文：Goldreich & Levin, *A Hard-Core Predicate for all One-Way Functions*, STOC 1989

---

## ⚠️ 存疑處

| 位置 | 問題 |
|---|---|
| **影片來源分散** | 本堂的內容散在 2018 的**四支**影片裡（L2、L4、L5、L6），而且順序與 Fall 2022 完全不同。各段對應見開頭的表。 |
| **三份逐字稿是自轉的** | L2、L4、L5 的 YouTube 字幕都是舊版（沒標點、漏字嚴重，L4 漏掉近三成內容），我用 Whisper `turbo` 重轉。品質好很多，但**人名會錯**：Goldreich–Levin → “Goldrack”、Chernoff → “Chernobyl”。數學內容一律以投影片為準。 |
| 投影片 p5, p10 | PDF 文字層有動畫疊印（p10 的 “HARDCORE BIT (Take 1)” 那段把兩個版本的句子交錯在一起）。我按語意重建，**請對照原 PDF 的圖**。 |
| 投影片 p26 | 這頁疊印最嚴重，`Pr 𝑥 Pr ← !0,1 ; 𝑟 ←...` 是兩行公式疊在一起。我判讀為「假設存在 predictor $P$ 成功率 $\ge \frac12 + 1/p(n)$」＋「要造出反轉器 $A$」。 |
| 投影片 p29 | 最後一行 `≥1−2[ 4 − +5 ! = + + 1/𝑝(𝑛)` 下標全壞。我按上下文還原成 $1 - 2\left[\frac14 - \frac{1}{2p(n)}\right] = \frac12 + \frac{1}{p(n)}$，算式是通的，但請對照原圖。 |
| 投影片 p28 | averaging argument 的證明是 “Exercise in counting”，**投影片沒寫**。 |
| 投影片 p31 | 真正的證明（$\frac12$ 版本）**整段留到下一講**（Fall 2022 的 lec07）。本筆記寫的思路來自 L5 的口述，**不是完整證明**。 |
| 投影片 p12, p23 | 兩個關鍵事實（「存在每個位元都好猜的 OWF」、「universal hardcore predicate 不存在」）都指向 **PS2**，投影片沒有證明。 |
| L4 的其餘部分 | L4 後半（約 [51:42] 之後）整段是「用 discrete log 證明最高位元是 hardcore」，屬 **lec07**。本筆記只引用了它在 [43:40]–[48:16] 對 hardcore predicate 的定義與動機。 |
