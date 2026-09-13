# Lecture 2 — Computational Security, Pseudorandom Generators

> **來源說明**
> - 投影片：`slides/lec02.pdf`（**Fall 2022**，43 頁）—— **主要來源**，內容完整。
> - 影片：2018 那套的 **L6「Pseudorandom Generators」**（<https://youtu.be/fdr6RKyjhEs>），補 PRG 定義的動機與隨機性來源那段。
>
> **⚠️ 影片對不上，要特別注意這一堂。**
>
> 播放清單的 L2 是「One-Way Functions」，那是 Fall 2022 **lec06** 的主題，不是這堂。
> 而且 **L2 那支沒有可用的逐字稿** —— YouTube 把它的語音誤判成西班牙文，英文字幕是從壞掉的辨識結果機器翻譯來的，整份是 `[Music]` 和亂碼（80 分鐘只有 289 條字幕）。
>
> 退而求其次用了 L6，它的字幕品質很好（有標點大小寫）。但 L6 只對應到本堂的一部分：
>
> | lec02.pdf | L6 有沒有 |
> |---|---|
> | p9–18 計算安全、negligible、security parameter | ❌ 沒有（原本應在 L2） |
> | p19–24 PRG 定義（三種等價講法） | ✅ 有，而且講得很好 |
> | p25–29 PRG ⟹ 加密（第一個 reduction） | ❌ 沒有 |
> | p30–35 PRG 怎麼造 | △ L6 講的是「從 OWF 造 PRG」，屬 Fall 2022 lec06 |
> | p36–38 隨機性是稀缺資源 | ✅ 有，還多講了 von Neumann 的技巧 |
> | p39–42 de-randomization | ❌ 沒有 |
>
> L6 後半大量在講 hybrid argument 和「從 OWF + hardcore bit 造 PRG」，那是 Fall 2022 的 **lec03 和 lec06/07**，**這份筆記不寫**。
>
> 標 `📎 補充` 的區塊不是課堂內容，是我額外加的。

---

## 一句話總結

**把對手從「全能」降級成「跑得動多項式時間」，Shannon 的詛咒就破了** —— 只要存在 pseudorandom generator，就能用 $n$-bit 的金鑰安全地加密 $n+1$ bits 的訊息。

---

## 這堂要回答什麼

lec01 的結論是一句壞消息：任何完美安全的加密，金鑰都得跟訊息一樣長。這堂問：

1. **要放寬什麼，才能繞過它？**（答：對手的計算能力）
2. 放寬之後，「安全」的新定義長什麼樣？（答：computational indistinguishability + negligible functions）
3. 有什麼工具能兌現這個新定義？（答：**PRG**）
4. 這個工具存在嗎？（答：不知道，但有兩條建構路線）

---

## 1. lec01 複習：把定義改寫成「猜世界」的遊戲

（投影片 p2–8）

### 複習

- Alice 和 Bob 有共同金鑰 $k$，演算法 $(\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$。
- Correctness：$\mathrm{Dec}(k, \mathrm{Enc}(k,m)) = m$。
- Security：**perfect secrecy = perfect indistinguishability**（等價）。
- One-time pad 達成了，但金鑰跟訊息一樣長。Shannon 定理說這逃不掉。

### 關鍵改寫：從「分布相等」變成「Eve 猜不中」

原本的 perfect indistinguishability 是在講**兩個機率分布相同**：

$$\forall m_0, m_1, c: \quad \Pr[E(\mathcal{K}, m_0) = c] = \Pr[E(\mathcal{K}, m_1) = c]$$

投影片 p6–8 分三步把它改寫成**一個對手 EVE 的遊戲**。這一步是純改寫、沒有改變意思，但**是整堂課後面所有東西的模板**，值得慢慢看：

**第一步（p6）** —— 把 EVE 當成 distinguisher，看她輸出 0 的機率：

$$\forall \text{EVE}, \forall m_0, m_1: \quad \Pr[\text{EVE}(c) = 0 \mid k \leftarrow \mathcal{K};\, c = E(k, m_0)] = \Pr[\text{EVE}(c) = 0 \mid k \leftarrow \mathcal{K};\, c = E(k, m_1)]$$

**第二步（p7）** —— 換成實驗式寫法（先跑實驗、冒號後看事件）。**意思完全一樣**，只是之後全課都用這個記法：

$$\Pr[k \leftarrow \mathcal{K};\, c = E(k, m_0) : \text{EVE}(c) = 0] = \Pr[k \leftarrow \mathcal{K};\, c = E(k, m_1) : \text{EVE}(c) = 0]$$

**第三步（p8）** —— 併成一個式子。丟一枚公正硬幣 $b$ 決定用哪個訊息，要求 EVE 猜中 $b$ 的機率**恰好是 $1/2$**：

$$\forall \text{EVE}, \forall m_0, m_1: \quad \Pr[k \leftarrow \mathcal{K};\, b \leftarrow \{0,1\};\, c = E(k, m_b) : \text{EVE}(c) = b] = \frac{1}{2}$$

> 💡 **「猜中的機率剛好是 1/2」= 完全沒有資訊。** 因為亂猜就能拿到 $1/2$。接下來整門課的安全定義幾乎都長這個樣子，只是把「$= 1/2$」換成「$\le 1/2 + (\text{很小的東西})$」。

---

## 2. 關鍵一步：計算能力有限的對手

（投影片 p9–10）

### 現代密碼學的公理

> **Feasible Computation = Probabilistic Polynomial-Time（p.p.t.）**
>
> （多項式是對 **security parameter $n$** 而言）

具體來說：

- **Alice 和 Bob** 是**固定的** p.p.t. 演算法（例如跑 $n^2$ 時間）。
- **Eve** 是**任意的** p.p.t. 演算法（$n^4$、$n^{100}$、$n^{10000}$ 都行）。

注意這個**不對稱**：誠實的一方時間固定；對手的多項式次數可以任意大，我們必須對**所有**多項式都安全。

> 投影片腳註：近年還要考慮 **quantum polynomial-time**。

### 這是「公理」而不是「定理」

這件事沒辦法證明。它是一個關於「現實世界什麼算做得到」的**建模假設**。整座現代密碼學的大樓蓋在上面。

---

## 3. Computational Indistinguishability（第一版）—— 以及它為什麼還不夠

（投影片 p11–12）

### 第一版：直接把 EVE 限制成 p.p.t.

$$\forall \textbf{p.p.t. } \text{EVE}, \forall m_0, m_1: \quad \Pr[k \leftarrow \mathcal{K};\, b \leftarrow \{0,1\};\, c = E(k, m_b) : \text{EVE}(c) = b] = \frac{1}{2}$$

跟 p8 一模一樣，只多了 **p.p.t.** 三個字。

### 但這樣還是做不到

投影片 p12 的標題就寫著：**Still subject to Shannon's impossibility!**

設定：訊息 $n+1$ bits，金鑰 $n$ bits（正是我們想要的那種「金鑰比訊息短」的方案）。

對任一個密文 $c$，看「所有可能解出 $c$ 的訊息」：

$$S_c = \{\, D(k, c) : k \in \mathcal{K} \,\}, \qquad |S_c| \le 2^n$$

但訊息一共有 $2^{n+1}$ 個。所以 $S_c$ **裝不下所有訊息** —— 一定有訊息跟 $c$ 不相容。

**Eve 的策略**（投影片原文）：隨機挑一把金鑰 $k$，算 $D(k,c)$，然後

- 若 $D(k,c) = m_0$，輸出 $0$ —— 這件事發生的機率 $\ge 1/2^n$
- 若 $D(k,c) = m_1$，輸出 $1$ —— 這件事發生的機率 $= 0$
- 都不是的話，丟硬幣

**結論**：$\Pr[\text{EVE 猜中}] \ge \dfrac{1}{2} + \dfrac{1}{2^{n+1}}$

> ⚠️ 這頁是一張圖 + 幾行字，完整論證是課堂口述的，而這堂**沒有可用影片**。我能確認的是投影片寫的策略和結論。細節上，$m_0$ 要挑成跟 $c$ 相容、$m_1$ 挑成跟 $c$ 不相容（由 $|S_c| < |\mathcal{M}|$ 保證存在這種訊息）。

### 這告訴我們什麼 —— 這才是重點

Eve 的優勢是 $1/2^{n+1}$，**指數小**，小到現實中完全沒意義。但第一版定義要求猜中機率**恰好等於 $1/2$**，所以 $1/2^{n+1} > 0$ 就已經違反定義了。

> **定義訂得太死。我們必須允許一點點誤差 —— 但「一點點」得先定義清楚。**

這就是下一節的動機。

---

## 4. Negligible Functions 與 Security Parameter

（投影片 p13–17）

### 定義

> **Definition.** 函數 $\mu: \mathbb{N} \to \mathbb{R}$ 是 **negligible（可忽略的）**，若對**每個**多項式函數 $p$，存在 $n_0$，使得對所有 $n > n_0$：
> $$\mu(n) < \frac{1}{p(n)}$$

白話：**比任何多項式的倒數都衰減得更快。**

### 為什麼是「這個」定義

投影片給的關鍵性質：

> **Key property: Events that occur with negligible probability look to poly-time algorithms like they never occur.**
>
> （以 negligible 機率發生的事件，在多項式時間演算法眼裡，等同於從來不會發生。）

直覺：多項式時間演算法最多跑 $p(n)$ 步、最多試 $p(n)$ 次。一件機率是 $\mu(n)$ 的事，試 $p(n)$ 次撞上的機率大約是 $p(n) \cdot \mu(n)$ —— 而依定義這仍然是 negligible。**所以它永遠撞不上。**

### 課堂測驗

**Q1（p14）：$\mu(n) = 1/n^{\log n}$ 是 negligible 嗎？**

**是。** 因為
$$n^{\log n} = 2^{(\log n)^2} \quad\text{而任何多項式}\quad n^c = 2^{c \log n}$$
$(\log n)^2$ 最終會超過 $c\log n$（對任何固定 $c$），所以 $n^{\log n}$ 最終比任何 $n^c$ 都大，倒數就更小。

（注意：它**不是**指數小的。它介於「多項式」和「指數」之間，這種叫 quasi-polynomial。negligible 不需要到指數等級。）

**Q2（p15）：**
$$\mu(n) = \begin{cases} 1/n^{100} & n \text{ 是質數} \\ 1/2^n & \text{否則} \end{cases}$$
**是 negligible 嗎？**

**不是。** 取多項式 $p(n) = n^{101}$。定義要求「對**所有**夠大的 $n$」都有 $\mu(n) < 1/n^{101}$。但只要 $n$ 是質數，$\mu(n) = 1/n^{100} > 1/n^{101}$。質數有無窮多個，所以不存在那個 $n_0$。

> 💡 **這題的用意**：negligible 是一個「對所有夠大的 $n$ 都成立」的條件，**不是「平均來說很小」**。只要有無窮多個 $n$ 違反，就出局。定義裡那兩個 quantifier 的順序不是裝飾。

**Q3（p16，PS1 作業題）：$\mu$ 是 negligible、$q$ 是多項式，$\mu(n) \cdot q(n)$ 還是 negligible 嗎？**

這題是 problem set 1 的題目，留給你自己做。
（提示：要證它比 $1/p(n)$ 小，去對 $\mu$ 套用哪一個多項式？）

這題的結論就是上面那條 Key property 的形式化版本 —— 它之後**會被反覆使用**。

### Security Parameter $n$（有時寫 $\lambda$）

（p17）整套框架的度量單位：

- **執行時間和成功機率都用 $n$ 的函數來衡量。**
- **要求**誠實的一方跑在 $n$ 的**固定**多項式時間內。
- **允許**對手跑在 $n$ 的**任意**多項式時間內。
- **要求**對手的成功機率（超出亂猜的部分）在 $n$ 之下是 negligible。

實務上 $n$ 就是「金鑰幾個 bit」那種東西 —— 課堂上舉的例子是 128。

---

## 5. Computational Indistinguishability（第二版）

（投影片 p18）

把第一版的「$= 1/2$」放寬成「$\le 1/2 + \mu(n)$」：

> $$\forall \textbf{p.p.t. } \text{EVE},\; \exists \text{ negligible } \mu,\; \forall m_0, m_1:$$
> $$\Pr[k \leftarrow \mathcal{K};\, b \leftarrow \{0,1\};\, c = E(k, m_b) : \text{EVE}(c) = b] \;\le\; \frac{1}{2} + \mu(n)$$

**注意 quantifier 的順序**：是「對每個 EVE，**存在**一個 negligible $\mu$」。也就是說**每個對手可以有自己的 $\mu$** —— 因為不同對手跑不同的多項式時間，優勢自然不同。

> 💡 這個式子是本門課的**模板**。之後每一個安全定義（PRG、PRF、MAC、簽章、公鑰加密…）幾乎都是它的變形：換掉兩個世界的定義，其餘照抄。

---

## 6. 第一個密碼學工具：Pseudorandom Generator (PRG)

（投影片 p19–24）

### 非正式說法

> **確定性**的程式，把一個「真隨機」的**短** seed，拉長成一串（長很多的）「看起來隨機」的 bits。

$$\text{seed} \;\longrightarrow\; \boxed{\text{PRG } G} \;\longrightarrow\; b_1 b_2 b_3 \dots$$

兩個問題：**「看起來隨機」怎麼定義？** 以及 **這種 $G$ 存在嗎？**

### 為什麼需要它（影片 L6 [0:53]–[8:29]）

密碼學到處都要隨機性 —— 選金鑰、每次加密都要。但真隨機很貴（見第 9 節）。所以我們想：**拿一小把真隨機（例如 128 bits），撐出一百萬 bits。**

輸出當然**不可能是真隨機的** —— Vinod 的說法是「我沒辦法無中生有創造 entropy」。$n$ bits 的 seed 只有 $2^n$ 種可能輸出，而 $m$ bits 的字串有 $2^m$ 種，$m > n$ 時絕大多數字串根本產不出來。

但它可以**夠隨機**。夠隨機是什麼意思？**只要對觀察它的人來說隨機就行了。**

### 三種定義

（投影片 p21。這頁有一道斜向的浮水印文字，拼起來是 **“ALL THREE DEFS ARE EQUIVALENT”**）

**Def 1 [Indistinguishability]**
> 沒有多項式時間演算法能區分「PRG 吃隨機 seed 的輸出」和「真隨機字串」。
> = 對所有實用目的而言，它「跟真隨機一樣好」。

**Def 2 [Next-bit Unpredictability]**
> 給定輸出的前 $i$ 個 bits，沒有多項式時間演算法能比亂猜更準地預測第 $i+1$ 個 bit。

**Def 3 [Incompressibility]**
> 沒有多項式時間演算法能把 PRG 的輸出壓縮成更短的字串（並還原回來）。

**三者等價。**

### 為什麼是 Def 1 —— 影片裡最好的一段（L6 [10:20]–[18:28]）

課堂上是一路試錯過來的，這個過程比結論更值得記：

**錯誤嘗試：列舉隨機字串的性質。** 早期（1970 年代）有人說：通過 chi-squared 檢定就算隨機。Vinod 的吐槽：「那如果它通過了 chi-squared，搞不好它過不了 chi-cubed 呢？誰知道？」

學生接著提了好幾個性質：不能預測下一個 bit；不能預測前一個 bit（隨機字串沒有方向性）；更一般地，給定任一子集合的 bits，不能預測子集合外的任何 bit；不可壓縮。

**問題在於：這些都只是「某一個」性質。** 你永遠不知道有沒有漏掉。

**破口 —— 回想圖靈測試（[15:59]）：**

> 「什麼叫電腦會思考？我不想去定義。難道是它乘兩個數字跟人一樣快？還是它認貓的照片跟一般人一樣準？**這些都是特定性質，沒有意義。**
>
> 你真正想說的是：**沒有任何演算法能區分「跟電腦互動」和「跟人互動」。** 那就一口氣形式化了人的**所有**性質。」

同一招套到隨機性上：**不要去列舉隨機字串的性質，而是要求「沒有人分得出來」** —— 這就一口氣涵蓋了所有性質。

Vinod 稱 indistinguishability 是 **“the king of definitions”（定義之王）**。

> 💡 這跟 lec01 那個 perfect indistinguishability 是同一個思路，而且跟 lec01 一樣 —— **多個定義等價，給我們信心抓對了概念。**

### 形式定義（Def 1）

（投影片 p22）

> **Definition [Indistinguishability].**
> 一個**確定性、多項式時間可計算**的函數 $G: \{0,1\}^n \to \{0,1\}^m$ 是 **PRG**，若：
>
> **(a) 會擴張（expanding）**：$m > n$；且
>
> **(b)** 對每個 PPT 演算法 $D$（稱為 **distinguisher** 或 **statistical test**），存在 negligible 函數 $\mu$ 使得
> $$\Big|\; \Pr[D(G(U_n)) = 1] \;-\; \Pr[D(U_m) = 1] \;\Big| \;=\; \mu(n)$$

記號：$U_n$（分別 $U_m$）表示 $n$-bit（分別 $m$-bit）字串上的均勻分布；$m$ 是 $m(n)$ 的簡寫。

兩個世界（p23）：

| WORLD 1：偽隨機世界 | WORLD 2：真隨機世界 |
|---|---|
| $y \leftarrow G(U_n)$ | $y \leftarrow U_m$ |

PPT distinguisher 拿到 $y$，分不出自己在哪個世界。

**怎麼讀這個式子**（影片 [19:13]–[20:06]）：把 $D$ 輸出 $1$ 想成「他喊：這是偽隨機的！」。定義要求：**餵他偽隨機字串時他喊的機率，跟餵他真隨機字串時他喊的機率，幾乎一樣。** 那他其實什麼也沒做到。

**一個技術細節（學生問的，[20:06]–[21:02]）**：嚴格來說我們要的是一整**族**函數 $\{G_n\}$ —— 64 bits 進、$64^2$ bits 出；65 bits 進、$65^2$ bits 出；以此類推。但寫成一族太累贅，所以照慣例只寫一個 $G$，$n$ 就是 security parameter。

### 為什麼這是個好定義（p24）

> **對所有應用都好用**：只要我們能找到真隨機的 seed，就可以在**任何**（多項式時間的）應用裡，把真隨機性換成 $\mathrm{PRG}(\text{seed})$。
>
> **理由**：如果那個應用換掉之後行為變了，那這個應用本身就構成了一個區分 $\mathrm{PRG}(\text{seed})$ 和真隨機字串的（多項式時間）statistical test —— 與 $G$ 是 PRG 矛盾。

這個論證非常漂亮：**應用本身就是 distinguisher。** 第 10 節的 de-randomization 就是它的直接應用。

---

## 7. PRG ⟹ 突破 Shannon 的困局

（投影片 p25–29）**這是你的第一個 reduction。**

### 方案：用 $n$-bit 金鑰加密 $n+1$ bits

- **$\mathrm{Gen}(1^n)$**：隨機產生 $n$-bit 金鑰 $k$
- **$\mathrm{Enc}(k, m)$**，$m$ 是 $(n+1)$-bit 訊息：
  - 把 $k$ 擴張成 $(n+1)$-bit 的偽隨機字串 $k' = G(k)$
  - 用 $k'$ 做 one-time pad：密文是 $k' \oplus m$
- **$\mathrm{Dec}(k, c)$**：輸出 $G(k) \oplus c$

**Correctness**：$G(k) \oplus c = G(k) \oplus G(k) \oplus m = m$ ✓

> 💡 **就是 one-time pad，只是 pad 換成偽隨機的。** 金鑰短了一個 bit —— 聽起來微不足道，但 lec01 證過「短一個 bit 都不可能」。所以這已經打破了 Shannon 的定理（在新的、放寬過的定義下）。

### 安全性證明：第一個 reduction

**反證法。** 假設存在 p.p.t. 對手 EVE、多項式 $p$、以及訊息 $m_0, m_1$，使得

$$\rho \;=\; \Pr\big[k \leftarrow \{0,1\}^n;\, b \leftarrow \{0,1\};\, c = G(k) \oplus m_b : \text{EVE}(c) = b\big] \;\ge\; \frac{1}{2} + \frac{1}{p(n)}$$

（也就是 EVE 的優勢**不是** negligible。）

**對照組**：如果 pad 是**真隨機**的，那就是貨真價實的 one-time pad，由 lec01 的結論，EVE 什麼都學不到：

$$\rho' \;=\; \Pr\big[k' \leftarrow \{0,1\}^{n+1};\, b \leftarrow \{0,1\};\, c = k' \oplus m_b : \text{EVE}(c) = b\big] \;=\; \frac{1}{2}$$

**關鍵**：$\rho \ne \rho'$，而兩者的差別**只在於 pad 是偽隨機還是真隨機**。所以 EVE 自己就能被改造成 $G$ 的 distinguisher。

**建構 distinguisher EVE′**（p28）：

> 輸入一個字串 $y$（$n+1$ bits）。
> 1. 隨機丟一枚硬幣得到 $b$。
> 2. 跑 $\text{EVE}(y \oplus m_b)$，設它的輸出是 $b'$。
> 3. 若 $b = b'$，輸出 **“PRG”**；否則輸出 **“RANDOM”**。

分析：

- **$y$ 是偽隨機**（$y = G(k)$）：EVE′ 餵給 EVE 的正好是真方案的密文，所以
  $$\Pr[\text{EVE′ 輸出 “PRG”}] = \rho \ge \frac{1}{2} + \frac{1}{p(n)}$$
- **$y$ 是真隨機**：EVE′ 餵的是貨真價實的 one-time pad 密文，所以
  $$\Pr[\text{EVE′ 輸出 “PRG”}] = \rho' = \frac{1}{2}$$

兩者相減：

$$\Pr[\text{EVE′ 輸出 “PRG”} \mid y \text{ 偽隨機}] - \Pr[\text{EVE′ 輸出 “PRG”} \mid y \text{ 真隨機}] \;\ge\; \frac{1}{p(n)}$$

$1/p(n)$ **不是** negligible，所以 EVE′ 區分開了 $G$ 的輸出和真隨機字串 —— 與 $G$ 是 PRG 矛盾。$\blacksquare$

> 💡 **把 reduction 的形狀記起來，之後會用幾十次：**
> 1. 假設有個對手打破了**方案**。
> 2. 把它當黑盒子，包一層，造出一個打破**底層工具**的演算法。
> 3. 底層工具的假設說那不可能 → 矛盾。
>
> 這就是 lec01 講的 “Science wins either way”。

### 留下的兩個問題（p29）

**$Q_1$：PRG 存在嗎？**
（練習：若 $P = NP$，則 PRG 不存在。）

**$Q_2$：更長的訊息、或同一把金鑰送多則訊息，怎麼辦？**
- **Length extension**：若存在「拉長一個 bit」的 PRG，就存在「拉長多項式個 bit」的 PRG。
- **Pseudorandom functions (PRF)**：擴張量是指數級、而且可以「隨機存取」輸出的 PRG。

兩個都是下一講的內容。

---

## 8. PRG 存在嗎？兩種建構路線

（投影片 p30–35）

### 實務路線（The Practical Methodology）

1. 從一個**設計框架**出發（例如：「適當選擇的函數、複合適當多次，看起來就是隨機的」）。
2. 提出一個**候選建構**（投影片舉 **Rijndael**，後來成為 **AES**）。
3. 做**大量的 cryptanalysis**（讓全世界來打，打不破就先用）。

### 基礎路線（The Foundational Methodology）—— 本課的主線

**歸約到更簡單的原語（primitive）。** 投影片畫的依賴圖：

```
           digital signatures      PRF
                        \         /
                         \       /
                          \     /
                           PRG
             hashing      /
                   \     /
                    \   /
                    OWF
                     |
     研究充分、average-case 困難的問題
```

> **“Science wins either way” — Silvio Micali**

所有東西最終架在 **one-way functions (OWF)** 上，而 OWF 又架在「被充分研究、平均情況下困難」的問題上。

> 📌 注意是 **average-case hard**，不是 worst-case hard。這個區別很重要 —— 密碼學需要「隨便抽一個實例都難」，而 NP-hardness 只保證「最壞的實例難」。lec01 提過這是這門課的副產品收穫之一。

### 一個具體候選：Subset-sum

（p35）

$$G(a_1, \dots, a_n, x_1, \dots, x_n) \;=\; \Big(a_1, \dots, a_n, \;\sum_{i=1}^{n} x_i a_i \bmod 2^{n+1}\Big)$$

其中 $a_i$ 是隨機的 $(n+1)$-bit 數字，$x_i$ 是隨機 bits。

**輸入**：$n(n+1) + n$ bits。**輸出**：$n(n+1) + (n+1)$ bits。確實有擴張（多了 1 個 bit）。

投影片稱它 **“Beautiful Function”**，因為：

- **若 $G$ 是 one-way function，則 $G$ 是 PRG。**（同一個函數同時是兩種東西 —— 很罕見）
- **若 lattice 問題在最壞情況下困難，則 $G$ 是 PRG。**（worst-case 硬度撐起 average-case 安全 —— 這是 lattice 密碼學的招牌性質，lec19 會回來談）

---

## 9. 隨機性是稀缺資源

（投影片 p36–38，影片 L6 [0:01]–[7:40]）

### 隨機性的用途

模擬 / 抽樣 / MCMC、分散式運算、機率演算法、**密碼學**。

### 我們的隨機 bits 從哪來？

1. **專用硬體**：例如電晶體雜訊。
2. **使用者輸入**：每次要用隨機數就去問使用者。（Vinod 舉例：在 MIT 網站上申請憑證時，它會叫你亂晃滑鼠。）
3. **量子性**（本課大致不談）。

**問題**：這些來源產出的 bits 通常是**有偏的（biased）**，不是均勻的。

### 為什麼有偏就完蛋（[1:38]）

拿 one-time pad 當例子：如果 pad 不是均勻隨機，而是每個 bit 有 $3/4$ 的機率是 1 —— **你立刻就開始從密文看到訊息的資訊了。** 我們的所有安全性都建立在「均勻隨機、獨立同分布」上。

### 📎 von Neumann 的技巧（1940 年代）

投影片只寫了一行 `[randomness extraction: von Neumann,…]`，影片 [2:26]–[5:54] 完整講了這個小謎題，很值得記：

**問題**：你有一串獨立的 bits $B_1, B_2, \dots, B_n$，每個是 1 的機率都是某個 $p$。你**不知道 $p$ 是多少**，甚至不知道它偏向哪一邊。怎麼萃取出真正均勻的 bits？

**學生的第一個答案：XOR 它們。** Vinod 的分析：若每個 bit 的偏差是 $\varepsilon$（即 $\Pr[=1] = 1/2 + \varepsilon$），XOR 兩個之後偏差變成 $\varepsilon^2$，XOR $k$ 個變成 $\varepsilon^k$。$k$ 大的時候偏差 negligible 地接近 0。
**這對本課的大部分場合其實已經夠好了**（我們本來就接受 negligible 的誤差）。但它**不是完美均勻**。

**von Neumann 的答案**：每次看**兩個** bits。

- 看到 `01` → 輸出 `1`
- 看到 `10` → 輸出 `0`
- 看到 `00` 或 `11` → **丟掉，往下看**

**為什麼對**：不管偏差 $p$ 是多少，只要 bits 獨立，
$$\Pr[01] = p(1-p) = \Pr[10]$$
兩者恰好相等。所以輸出完美均勻。

**代價**：你丟掉了大量的 bits（輸出最多 $n/2$，實際還更少）。

> 💡 **一個 trade-off**：XOR 給你比較多輸出但只是 negligible 接近均勻；von Neumann 給你比較少輸出但完美均勻。

**現實中更難**：Vinod 提醒，他假設了 bits 之間獨立，但現實中沒有東西是獨立的 —— 「我現在的按鍵和半秒後的按鍵並不獨立」。處理這種情況是 **randomness extractors** 這整個研究領域，它連結到 coding theory、list-decodable codes、以及之後會學到的 Goldreich–Levin。

### 結論

> **真隨機性是昂貴的商品。** 這就是為什麼我們需要 PRG。

---

## 10. 應用：De-randomization

（投影片 p39–42）

PRG 不只對密碼學有用，對複雜度理論也有話要說。

### 設定

回想 $L \in BPP$ 表示存在多項式時間演算法 $M$ 使得：

$$x \in L \;\Longrightarrow\; \Pr_{y \leftarrow U_m}[M(x,y) \text{ accepts}] > 2/3$$
$$x \notin L \;\Longrightarrow\; \Pr_{y \leftarrow U_m}[M(x,y) \text{ accepts}] < 1/3$$

**想法**：不要用 $m$ 個真隨機 bits，改用 PRG 從一個短 seed 生出 $y$。

$$\text{seed} \to \boxed{G} \to y \to \boxed{M(x,y)}$$

### 定理 1

> **Theorem.** 若 PRG 存在，則 $BPP \subseteq \bigcap_{\varepsilon > 0} TIME\big(2^{n^{\varepsilon}}\big)$。
>
> 白話：若 PRG 存在，則任何隨機化多項式時間演算法，都能用**確定性的次指數時間**模擬。

**證明概要**：用一個從 $n = m^{\varepsilon}$ bits 擴張到 $m$ bits 的 PRG。則

$$x \in L \;\Longrightarrow\; \Pr_{\text{seed } y}[M(x, G(y)) \text{ accepts}] > \tfrac{2}{3} - \mu(n)$$
$$x \notin L \;\Longrightarrow\; \Pr_{\text{seed } y}[M(x, G(y)) \text{ accepts}] < \tfrac{1}{3} + \mu(n)$$

**為什麼？如果上面不成立，$M$ 本身就是 $G$ 的 distinguisher！**（正是 p24 那個論證。）

投影片特別註記：$M$ 是一個**已知的、固定的、固定多項式時間的** distinguisher —— 這正好落在 PRG 定義涵蓋的範圍內。

**確定性演算法長這樣**（p41）：

$$x \in L \;\Longrightarrow\; \#\{\text{seed } y : M(x, G(y)) \text{ accepts}\} > 0.65 \cdot 2^n = 0.65 \cdot 2^{m^{\varepsilon}}$$
$$x \notin L \;\Longrightarrow\; \#\{\text{seed } y : M(x, G(y)) \text{ accepts}\} < 0.35 \cdot 2^{m^{\varepsilon}}$$

**枚舉所有的 seed $y$**，跑 $M(x, G(y))$，數有幾個 accept。超過 $0.65 \cdot 2^{m^\varepsilon}$ 就接受，否則拒絕。

**完全沒有用到隨機性。** 代價是枚舉 $2^{m^{\varepsilon}}$ 個 seed —— 次指數時間。

### 定理 2

> **Theorem.** 若「指數級安全」的 PRG 存在，則 $BPP = P$。

**證明概要**：用一個從 $n = O(\log m)$ bits 擴張到 $m$ bits 的 PRG，而且要求它不只騙得過 $\mathrm{poly}(n)$ 時間的演算法，還要騙得過 $2^{c_1 n} = m^{c_2}$ 時間的演算法。

前一個證明原封不動套用（投影片用了 *mutatis mutandis*，意思是「做必要的修改後」），**關鍵是隨機化演算法（對我們而言就是對手）跑在固定的多項式時間內**。

seed 只有 $O(\log m)$ bits，所以枚舉只要 $2^{O(\log m)} = \mathrm{poly}(m)$ 時間 —— 真正的多項式時間。

> 💡 **一個很值得想的結論**：如果密碼學的假設成立（強 PRG 存在），那麼**隨機性對多項式時間運算來說根本沒有增加威力**。密碼學的困難假設，反過來給了複雜度理論一個結論。

---

## 下一講（p43）

$Q_2$：同一把金鑰怎麼加密更長的訊息、或多則訊息？

1. **PRG length extension**
2. **Pseudorandom functions (PRF)**，以及 PRG ⟹ PRF

---

## 名詞對照表

| 英文 | 中文 | 說明 |
|---|---|---|
| p.p.t. (probabilistic polynomial-time) | 機率性多項式時間 | 現代密碼學對「做得到的運算」的定義 |
| security parameter $n$（或 $\lambda$） | 安全參數 | 一切時間與機率的度量基準 |
| computational indistinguishability | 計算不可區分性 | 沒有 p.p.t. 演算法能分辨兩個分布 |
| negligible function | 可忽略函數 | 比任何多項式倒數衰減更快 |
| distinguisher / statistical test | 區分器 / 統計檢定 | 試圖分辨兩個世界的演算法 |
| advantage | 優勢 | 猜中機率超出 $1/2$ 的部分 |
| pseudorandom generator (PRG) | 偽隨機產生器 | 確定性地把短 seed 拉長 |
| seed | 種子 | PRG 的（真隨機）輸入 |
| expanding / stretch | 擴張 / 拉伸量 | $m > n$；$m - n$ 是拉伸量 |
| next-bit unpredictability | 下一位元不可預測性 | PRG 的等價定義 2 |
| incompressibility | 不可壓縮性 | PRG 的等價定義 3 |
| $U_n$ | — | $n$-bit 字串上的均勻分布 |
| reduction | 歸約 | 把「打破方案」轉成「打破底層工具」 |
| one-way function (OWF) | 單向函數 | 整座大樓的地基（lec06） |
| average-case hardness | 平均情況困難 | 隨便抽一個實例都難 |
| worst-case hardness | 最壞情況困難 | 只保證存在難的實例（較弱） |
| randomness extractor | 隨機性萃取器 | 從有偏來源萃取均勻 bits |
| de-randomization | 去隨機化 | 用 PRG 把隨機演算法變確定性 |
| BPP | — | 有界錯誤機率多項式時間 |
| mutatis mutandis | 做必要修改後 | 投影片 p42 的拉丁文 |

---

## 📎 外部補充（非課堂內容）

> 以下不在投影片、也不在 L6 影片裡，是我額外加的。

**1. Negligible 為什麼不直接定義成「指數小」**
用「比所有多項式倒數都小」而不是 $2^{-n}$，是因為它對「乘以多項式」封閉（就是 PS1 那題），也對「加上多項式多個」封閉。這讓 union bound 和 hybrid argument 用起來很順。$1/n^{\log n}$ 就是一個 negligible 但不是指數小的例子（課堂 Q1）。

**2. 「$\exists \mu$ 在 $\forall$ EVE 之後」的意義**
這個順序讓每個對手可以有自己的誤差函數。反過來寫（先固定一個 $\mu$ 對所有對手成立）會是更強的要求，而且因為對手的多項式次數可以任意大，那樣通常做不到。

**3. 第 7 節那個方案只安全「一次」**
用 $G(k)$ 當 pad，和 one-time pad 一樣**不能重用金鑰** —— 兩則訊息用同一個 $k$，$c_0 \oplus c_1 = m_0 \oplus m_1$ 一樣會洩漏（lec01 第 7 節）。這正是 $Q_2$ 要解決的問題。

**4. $P = NP$ ⟹ 沒有 PRG（p29 的練習）**
概念上：若 $P = NP$，那麼「存在一個 seed $s$ 使得 $G(s) = y$」這個 NP 敘述可以在多項式時間內判定。distinguisher 就直接問這個問題 —— 偽隨機字串永遠答「是」，而真隨機的 $m$-bit 字串答「是」的機率最多 $2^n/2^m$，很小。

**5. 延伸閱讀**
- Katz–Lindell，第 3 章（computational security、PRG）
- Boneh–Shoup（在 `books/`），第 3 章
- Goldreich，*Foundations of Cryptography* Vol. 1，第 3 章（pseudorandomness 的標準處理）

---

## ⚠️ 存疑處

| 位置 | 問題 |
|---|---|
| **整堂課的影片** | 播放清單 L2 是「One-Way Functions」（= Fall 2022 lec06），不是這堂。而且**那支沒有可用逐字稿** —— YouTube 把它的語音誤判成西班牙文（`es-orig`），英文軌是從壞掉的辨識結果機器翻譯的，80 分鐘只有 289 條字幕，內容是 `[Music]` 和亂碼。本筆記的影片內容全部來自 L6。 |
| 投影片 p12 | 「為什麼第一版定義仍然做不到」是一張圖 + 幾行字，完整論證是課堂口述的，**沒有影片可對**。我照投影片原文寫了 Eve 的策略和結論 $\ge 1/2 + 1/2^{n+1}$，並補上「$m_0$ 要與 $c$ 相容、$m_1$ 不相容」這個必要條件。若要嚴格，建議自己重推一次。 |
| 投影片 p13–17 | negligible 的定義在 PDF 文字層裡是錯位的（`for all sufficiently` 和 `there exists an` 兩行疊在一起）—— 那是投影片動畫的兩個版本疊印。正確讀法是「**存在 $n_0$，對所有 $n > n_0$**」。 |
| 投影片 p21 | 斜向的浮水印文字拼起來是 “ALL THREE DEFS ARE EQUIVALENT”。PDF 文字層把它拆成碎片（`T`、`EN`、`IVA`、`QU`…），不是亂碼。 |
| 投影片 p22 | 定義寫的是 `if there is a negligible function 𝝁 such that ... = 𝝁(n)`，前面多了一個 `if`，應是筆誤。而且慣例上寫 $\le \mu(n)$ 比 $= \mu(n)$ 好。 |
| 投影片 p35 | subset-sum 的下標在 PDF 文字層裡是壞的（`∑%./"` 之類）。我按標準寫法還原成 $\sum_{i=1}^{n} x_i a_i \bmod 2^{n+1}$，請對照原始 PDF 的圖確認。 |
| 投影片 p40–42 | 指數的文字層同樣有損（`2 "!`、`20" %`）。我按上下文還原為 $2^{n^{\varepsilon}}$ 與 $2^{c_1 n} = m^{c_2}$，常數的確切寫法請對照原 PDF。 |
| lec02 vs L6 | L6 後半（hybrid argument、next-bit ⟹ indistinguishability 的證明、從 OWF + hardcore bit 造 PRG）**不屬於本堂**，是 Fall 2022 的 lec03 與 lec06/07。本筆記依 BRIEF 的規則沒有寫進來。 |
