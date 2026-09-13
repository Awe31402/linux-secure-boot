# Lecture 3 — Hybrid Arguments, Length Extension, Pseudorandom Functions

> **來源說明**
> - 投影片：`slides/lec03.pdf`（**Fall 2022**，44 頁）—— **主要來源**。
> - 影片（都是 2018 那套）：
>   - **L6「Pseudorandom Generators」**（<https://youtu.be/fdr6RKyjhEs>）—— 補前半：next-bit unpredictability、**hybrid argument**。字幕品質好（有標點）。
>   - **L7「Pseudorandom Functions」**（<https://youtu.be/SmIQNWXkxeQ>）—— 補後半：stateful → stateless、**PRF**。字幕是舊版差品質（無標點、人名地名大量錯誤），但數學內容能用投影片校正。
>
> 這堂的影片對應**比 lec02 好**：兩支加起來涵蓋了本堂絕大部分內容。
>
> ⚠️ 但兩支都夾帶了別堂的東西：
> - L6 的前半是 PRG 定義（= **lec02**）。
> - L7 的後半是 **GGM 樹狀建構（PRG ⟹ PRF）**，那是 Fall 2022 的 **lec04**。投影片 p44 明講「Theorem (next lec)」。**本筆記不寫。**
>
> 標 `📎 補充` 的區塊不是課堂內容，是我額外加的。

---

## 一句話總結

**把大問題切成一串只差一點點的小步驟（hybrid argument），就能證明「猜不到下一個 bit」和「分不出來」是同一件事** —— 有了這個工具，PRG 可以拉長到任意長度，再進一步做出 **PRF**，最後得到不需要記狀態、能用同一把金鑰加密無數則訊息的加密方案。

---

## 這堂要回答什麼

lec02 結束在一個限制：PRG 讓我們能用 $n$-bit 金鑰加密**一則**比金鑰長的訊息。但：

> **同一把金鑰，怎麼加密（多項式）多則訊息？**

兩條路：

1. **PRG length extension** → 得到 **stateful（有狀態的）**多訊息加密。
2. **Pseudorandom Functions (PRF)** → 得到 **stateless（無狀態的）**多訊息加密。

而要走第 1 條路，得先補一個工具：**hybrid argument**。

---

## 0. lec02 複習（p2）

- **Computational indistinguishability**：秘密金鑰加密的新安全定義。（新概念：p.p.t. 對手、negligible functions）
- **後果**：Shannon 的不可能性定理不再適用。
- **新工具**：Pseudorandom Generator (PRG)。
- **PRG ⟹ 可以加密一則比金鑰長的訊息。**
- 看過一個 PRG 建構（基於 subset-sum）。課程後面還會有很多。

---

## 1. 準備工作：Next-bit Unpredictability 的正式定義

（投影片 p4–7）

lec02 提過偽隨機性的三種定義（p5 那頁的斜向浮水印又出現了：**“ALL THREE DEFS ARE EQUIVALENT”**）：

- **Def 1 [Indistinguishability]**：沒有多項式時間演算法能區分 PRG 輸出和真隨機字串。
- **Def 2 [Next-bit Unpredictability]**：沒有多項式時間演算法能從前 $i$ 個 bits 比亂猜更準地預測第 $i+1$ 個 bit。
- **Def 3 [Incompressibility]**：沒有多項式時間演算法能把輸出壓縮。

lec02 只正式定義了 Def 1。這堂把 Def 2 也寫出來，然後證明兩者等價。

### Def 1 複習（p6）

> 確定性、多項式時間可計算的 $G: \{0,1\}^n \to \{0,1\}^m$ 是 **indistinguishable** 的，若對每個 PPT distinguisher $D$，存在 negligible $\mu$：
> $$\Big|\Pr[D(G(U_n)) = 1] - \Pr[D(U_m) = 1]\Big| = \mu(n)$$

### Def 2 正式定義（p7）

> 確定性、多項式時間可計算的 $G: \{0,1\}^n \to \{0,1\}^m$ 是 **next-bit unpredictable** 的，若對每個 PPT 演算法 $P$（稱為 **next-bit predictor**）和**每個** $i \in \{1, \dots, m\}$，存在 negligible $\mu$：
> $$\Pr\big[y \leftarrow G(U_n) : P(y_1 y_2 \dots y_{i-1}) = y_i\big] = \frac{1}{2} + \mu(n)$$

記號：$y_1, y_2, \dots, y_m$ 是 $m$-bit 字串 $y$ 的各個 bit。

注意：$P$ 只拿到**前綴**，要猜**下一個** bit。亂猜是 $1/2$，所以「只能贏 negligible 那麼多」就是「等於沒贏」。

---

## 2. 定理：Def 1 ⟺ Def 2

（投影片 p8–24）

> **THEOREM.** 一個 PRG $G$ 是 indistinguishable 的**若且唯若**它是 next-bit unpredictable 的。
>
> 換個說法（p9）：$G$ 通過**所有**（多項式時間）statistical tests，若且唯若它通過（多項式時間）**next-bit tests**。

### 為什麼這件事令人驚訝（p10, p24）

- **NBU 看起來弱得多。** 它只說「next-bit predictor 這**一種特定類型**的 distinguisher 沒辦法成功」。
- **但它們竟然相等。** 擋住這一種，就等於擋住了全部。
- **而且 NBU 通常好用得多** —— 要證一個東西是 PRG，去證 NBU 常常簡單很多。

> 💡 這跟 lec01「兩個安全定義等價」、lec02「三個偽隨機定義等價」是同一種戲碼。密碼學一直在做這件事。

---

### 方向 1：Indistinguishability ⟹ NBU（簡單的那邊）

（p11–15）反證法。

**假設**存在 p.p.t. predictor $P$、多項式 $p$、以及某個 $i$：

$$\Pr[y \leftarrow G(U_n) : P(y_1 \dots y_{i-1}) = y_i] \;\ge\; \frac{1}{2} + \frac{1}{p(n)}$$

**造 distinguisher $D$**：輸入一個 $m$-bit 字串 $y$，

1. 在前綴 $y_1 y_2 \dots y_{i-1}$ 上跑 $P$。
2. 若 $P$ 猜中了第 $i$ 個 bit $y_i$，輸出 $1$（「PRG」）；否則輸出 $0$（「Random」）。

**$P$ 是 p.p.t.，所以 $D$ 也是。**

**分析**：

- $y$ 來自 PRG：
  $$\Pr[y \leftarrow G(U_n) : D(y) = 1] = \Pr[y \leftarrow G(U_n) : P(y_1 \dots y_{i-1}) = y_i] \;\ge\; \frac{1}{2} + \frac{1}{p(n)}$$
  （第一個等號是 $D$ 的定義；不等號是對 $P$ 的假設。）

- $y$ 是真隨機：
  $$\Pr[y \leftarrow U_m : D(y) = 1] = \Pr[y \leftarrow U_m : P(y_1 \dots y_{i-1}) = y_i] = \frac{1}{2}$$
  （**因為 $y$ 是隨機的** —— $y_i$ 跟前綴獨立，任何演算法猜中的機率都恰好是 $1/2$。）

相減：

$$\Big|\Pr[y \leftarrow G(U_n) : D(y) = 1] - \Pr[y \leftarrow U_m : D(y) = 1]\Big| \;\ge\; \frac{1}{p(n)}$$

不是 negligible，矛盾。$\blacksquare$

> 💡 這個方向簡單，因為 **next-bit predictor 本來就是一種 distinguisher** —— 只要把「猜中沒」翻譯成「輸出 0 還是 1」就好。

---

### 方向 2：NBU ⟹ Indistinguishability（難的那邊）

（p16–23）

**假設**存在 distinguisher $D$ 和多項式 $p'$：

$$\Pr[y \leftarrow G(U_n) : D(y) = 1] - \Pr[y \leftarrow U_m : D(y) = 1] \;\ge\; \frac{1}{p'(n)} \;=:\; \varepsilon$$

**我要從 $D$ 造出一個 next-bit predictor $P$。但怎麼造？!**（投影片 p16 原文的驚嘆號）

**難點在哪**：$D$ 只會對整串 $m$-bit 字串說「像 / 不像」。它**沒有告訴你哪一個 bit 出賣了它**。而 predictor 要的是「某一個特定位置的 bit」。

**兩個步驟**：

- **STEP 1：HYBRID ARGUMENT**（把「整串的差異」逼成「某單一個 bit 的差異」）
- **STEP 2：從「區分」變成「預測」**

---

#### 先看一個小 puzzle（p18）

> **Lemma.** 設 $p_0, p_1, p_2, \dots, p_m$ 是實數，滿足 $p_m - p_0 \ge \varepsilon$。
> 則**存在**一個下標 $i$ 使得 $p_i - p_{i-1} \ge \varepsilon / m$。

**Proof.** 望遠鏡（telescoping）展開：

$$p_m - p_0 = (p_m - p_{m-1}) + (p_{m-1} - p_{m-2}) + \dots + (p_1 - p_0) \;\ge\; \varepsilon$$

$m$ 項加起來至少是 $\varepsilon$，所以**至少有一項**至少是 $\varepsilon/m$（平均原理）。$\blacksquare$

影片裡 Vinod 問學生「這個敘述的證明，兩個字」，學生答 **“triangle inequality”**（[33:26]）。他也給了反證版本（[35:15]）：假設每一項都 $< \varepsilon/m$，那全部加起來 $< \varepsilon$，與假設矛盾。

> 💡 **這就是 hybrid argument 的全部數學內容 —— 真的就這麼簡單。** Vinod 的評語：「Profound? Not really. Pretty simple. **But this is the core of a hybrid argument: chop things into smaller steps.**」
>
> 困難的從來不是這條引理，而是**想出要怎麼切**。

---

#### STEP 1：Hybrid Distributions（p19–21）

**定義一串分布**，從「全隨機」一步一步走到「全偽隨機」：

$$H_0 = U_m \quad\text{(全部 $m$ 個 bit 都是真隨機)}$$
$$H_i = \underbrace{y_1 y_2 \dots y_i}_{\text{來自 } G(U_n)} \;\|\; \underbrace{u_{i+1} \dots u_m}_{\text{真隨機}}$$
$$H_m = G(U_n) \quad\text{(全部都是偽隨機)}$$

**關鍵：$H_{i-1}$ 和 $H_i$ 只差在第 $i$ 個 bit。** 在 $H_i$ 裡它是偽隨機的 $y_i$；在 $H_{i-1}$ 裡它是真隨機的 $u$。其餘完全一樣。

令 $p_i = \Pr[D(H_i) = 1]$。於是

$$p_0 = \Pr[D(U_m) = 1], \qquad p_m = \Pr[D(G(U_n)) = 1], \qquad p_m - p_0 \ge \varepsilon$$

**套用上面的 Lemma**：存在 $i$ 使得

$$p_i - p_{i-1} \;\ge\; \frac{\varepsilon}{m}$$

**關鍵直覺（p20 原文）**：

> $D$ 在**第 $i$ 個 bit 是偽隨機**時輸出 $1$ 的頻率，比它在**第 $i$ 個 bit 是真隨機**時更高。
>
> 所以 **$D$ 給了我們一個「訊號」**，告訴我們某個 bit 是不是「正確的第 $i$ 個 bit」。

**Vinod 怎麼描述這個定義（L6 [30:52]–[31:46]）**：

> 「第一個 hybrid 就是 PRG 的輸出本身，全紅。另一個極端是全部真隨機，全藍。現在我要**用一連串小步驟**從全紅走到全藍。什麼是一小步？把 PRG 的輸出算出來，**把最後一個 bit 砍掉，換成一個真正均勻的 bit**。下一個 hybrid？砍掉最後兩個，換成兩個真隨機的。這樣走下去，$m$ 步就到了。」

他也直接說了為什麼要這樣做（[32:39]）：

> 「重點是你**不想**面對那一整條長字串、去爭論它像這個還是像那個。你想用 triangle inequality 來論證。**這就是一開始要定義這些 hybrid 的理由。**」

---

#### 再往下挖一層（p21）

現在我們知道 $p_i - p_{i-1} \ge \varepsilon/m$。但這還不夠 —— 我們要的是「猜 $y_i$」。

**定義 $\widetilde{H}_i$**：跟 $H_i$ 完全一樣，只是把第 $i$ 個 bit **翻轉**成 $\widetilde{y_i} = 1 - y_i$（「錯的那個 bit」）。令 $\widetilde{p_i} = \Pr[D(\widetilde{H}_i) = 1]$。

> **Claim.** $\displaystyle p_{i-1} = \frac{p_i + \widetilde{p_i}}{2}$

**為什麼**：在 $H_{i-1}$ 裡，第 $i$ 個 bit 是一個**均勻隨機**的 bit $u$。它有 $1/2$ 機率等於 $y_i$（那就變成 $H_i$），有 $1/2$ 機率等於 $\widetilde{y_i}$（那就變成 $\widetilde{H}_i$）。所以 $H_{i-1}$ 就是這兩個分布的**等比例混合**。

> **Corollary (\*).** $\displaystyle p_i - \widetilde{p_i} \;\ge\; \frac{2\varepsilon}{m}$

**推導**：

$$\frac{\varepsilon}{m} \le p_i - p_{i-1} = p_i - \frac{p_i + \widetilde{p_i}}{2} = \frac{p_i - \widetilde{p_i}}{2} \quad\Longrightarrow\quad p_i - \widetilde{p_i} \ge \frac{2\varepsilon}{m}$$

**Takeaway（p21 原文）**：

> **餵給 $D$「對的 bit」時，它說 “1” 的頻率比餵「錯的 bit」時更高。**

**這就是可以拿來預測的訊號了。**

---

#### STEP 2：造出 Predictor $P$（p22）

**想法**：$P$ 拿到前 $i-1$ 個偽隨機 bits $y_1 y_2 \dots y_{i-1}$，要猜第 $i$ 個。

> **Predictor $P$：**
> 1. 隨機挑一個 bit $b$。
> 2. 餵 $D$ 輸入 $y_1 y_2 \dots y_{i-1} \; b \; u_{i+1} \dots u_m$（後面的 $u$ 都是隨機的）。
> 3. 若 $D$ 說 “1”，輸出 $b$ 當作對 $y_i$ 的預測；若 $D$ 說 “0”，輸出 $\bar{b}$。

**為什麼這樣做**：由 Takeaway，$D$ 說 “1” 傾向代表「你餵的那個 bit 是對的」。所以 $D$ 說 1 就相信 $b$，$D$ 說 0 就反過來猜。

---

#### 分析（p23）

$$
\begin{aligned}
&\Pr\big[x \leftarrow \{0,1\}^n;\, y = G(x) : P(y_1 \dots y_{i-1}) = y_i\big] \\[2pt]
&= \Pr[D(y_1 \dots y_{i-1} b \dots) = 1 \mid b = y_i]\cdot\Pr[b = y_i] \;+\; \Pr[D(y_1 \dots y_{i-1} b \dots) = 0 \mid b \ne y_i]\cdot\Pr[b \ne y_i] \\[4pt]
&= \frac{1}{2}\Big( \Pr[D(y_1 \dots y_{i-1} b \dots) = 1 \mid b = y_i] + \Pr[D(y_1 \dots y_{i-1} b \dots) = 0 \mid b \ne y_i] \Big) && (\Pr[b = y_i] = \tfrac12) \\[4pt]
&= \frac{1}{2}\Big( \Pr[D(y_1 \dots y_{i-1} y_i \dots) = 1] + \Pr[D(y_1 \dots y_{i-1} \widetilde{y_i} \dots) = 0] \Big) \\[4pt]
&= \frac{1}{2}\Big( p_i + \big(1 - \widetilde{p_i}\big) \Big) && (\Pr[\cdot = 0] = 1 - \Pr[\cdot = 1]) \\[4pt]
&= \frac{1}{2}\Big( 1 + \underbrace{(p_i - \widetilde{p_i})}_{\ge\, 2\varepsilon/m \text{ by } (*)} \Big) \\[4pt]
&\ge \frac{1}{2} + \frac{\varepsilon}{m} \;=\; \frac{1}{2} + \frac{1}{m \cdot p'(n)}
\end{aligned}
$$

$m \cdot p'(n)$ 是多項式，所以 $1/(m \cdot p'(n))$ **不是** negligible。$P$ 打破了 NBU，矛盾。$\blacksquare$

> 💡 **整個論證的形狀，值得背下來：**
> 1. 定義一串 hybrid，兩端分別是你想比較的兩個分布，相鄰兩個只差**一個**小地方。
> 2. 用 telescoping + 平均原理：既然兩端差 $\varepsilon$，就有**某一對**相鄰的差 $\varepsilon/m$。
> 3. 針對那一個小地方，把 distinguisher 改造成攻擊工具。
>
> 這門課之後會用這招**幾十次**。

### 一個練習（p24）

> **Exercise:** Previous-bit Unpredictability = Indistinguishability。

（也就是把「從前綴猜下一個」換成「從後綴猜前一個」，結論一樣。隨機字串沒有方向性 —— 這正是 lec02 課堂上學生提過的觀察。）

---

## 3. PRG Length Extension：一個 bit 變很多 bits

（投影片 p25–31）

> **THEOREM.** 若存在只拉長**一個 bit** 的 PRG，就存在拉長**多項式多個 bit** 的 PRG。

### 建構

設 $G: \{0,1\}^n \to \{0,1\}^{n+1}$ 是 PRG。造 $G'$：

```
seed = s₀ ──G──▶ s₁ ──G──▶ s₂ ──G──▶ … ──G──▶ s_{t-1} ──G──▶ s_t
                  │         │                   │             │
                  b₁        b₂                 b_{t-1}        b_t

輸出：b₁ b₂ b₃ b₄ b₅ … b_t  s_t
```

每一步：把 $G(s_{j-1})$ 的 $n+1$ bits 輸出**拆成兩段** ——

$$G(s_{j-1}) = \underbrace{b_j}_{1 \text{ bit，吐出去}} \;\|\; \underbrace{s_j}_{n \text{ bits，留著當下一輪的 seed}}$$

跑 $t$ 輪，就吐出 $t$ 個 bits，最後再把 $s_t$ 也輸出。總共 $t + n$ bits，而輸入只有 $n$ bits。**$t$ 可以是任意多項式。**

> **實務界管這個叫 stream cipher（串流加密法）。**

### 安全性證明（p31，留作練習）

> **Proof of Security (exercise): Use next-bit (or previous-bit?) unpredictability!**

投影片把證明留成練習，而且**明確提示要用 NBU** —— 這正是第 2 節那個等價定理的用途：**直接證 indistinguishability 很麻煩，證 NBU 容易得多。**

> 📎 提示裡那個「(or previous-bit?)」不是隨口說的。這個建構是**往前跑**的：早期的 $b_j$ 由早期的 state 決定。所以拿「後面的輸出去猜前面的」會比較自然。p24 那個練習就是在替這裡鋪路。

---

## 4. Stateful Encryption：用同一把金鑰加密多則訊息

（投影片 p32–35）

### 做法

Alice 和 Bob **都持有初始狀態 $s_0$**（就是金鑰），各自跑同一條 $G$ 鏈產生 $b_1, b_2, b_3, \dots$。

每次要加密，就**從沒用過的地方接著取 pad**：

| 時間 | 訊息 | 用掉的 pad bits | 之後的狀態 |
|---|---|---|---|
| 第一次 | 1-bit $m$ | $b_1$ | $s_1$ |
| 第二次 | 3-bit $m'$ | $b_2 b_3 b_4$ | $s_4$ |
| 第三次 | 1-bit $m''$ | $b_5$ | $s_5$ |

密文分別是 $m \oplus b_1$、$m' \oplus b_2b_3b_4$、$m'' \oplus b_5$。

**每個 pad bit 只用一次** —— 所以它真的是 one-time pad，只是 pad 是偽隨機的。

### 好處與壞處（p35）

**PLUS**：Alice 和 Bob 想加密幾個 bit 就加密幾個 bit，沒有上限。

**MINUS**：

> **Alice 和 Bob 必須讓狀態保持完美同步。他們不能同時傳送。**
>
> **一旦失去同步：正確性完蛋，安全性也一起完蛋。**

失去同步為什麼兩個都壞掉：

- **正確性**：Bob 用錯位置的 pad 去解，解出垃圾。
- **安全性**：如果兩人同時各自發訊息，**兩則訊息會用到同一段 pad** —— 就是 lec01 第 7 節那個 two-time pad 問題，$c_0 \oplus c_1 = m_0 \oplus m_1$ 直接洩漏。

**這就是我們要 stateless 的原因。**

---

## 5. 兩個「好的壞主意」

（投影片 p36–38，影片 L7 [22:29]–[28:53]）

投影片 p38 的標題原本寫「But these are good bad ideas…」—— 兩個都行不通，但**它們失敗的方式正好指出了 PRF 的定義**。

### 壞主意 #1：在多項式長的字串裡隨機挑位置（p36）

**想法**：金鑰 $k = s_0$ 展開成一條**多項式長**的偽隨機字串 $b_1 b_2 \dots b_{n^{100}}$。要加密時，**隨機挑一個位置**（比方說 5），送出

$$(\,5,\; m \oplus b_5\,)$$

Bob 收到就知道要用第 5 個 bit 解。**不需要記狀態** —— 位置寫在密文裡。

**為什麼不行：碰撞（Collisions）。**

$$\Pr[\text{Alice 前兩次挑到同一個位置}] \;\ge\; \frac{1}{n^{100}}$$

$1/n^{100}$ 是多項式的倒數，**不是 negligible**。一旦碰撞，Alice 就把同一個 one-time pad bit 用了兩次 —— 再次回到 two-time pad 的災難。

### 壞主意 #2：把字串加長到指數長（p37）

**想法**：那就把字串拉到 $2^n$ 那麼長，$b_1 b_2 \dots b_{2^n}$。

碰撞機率變成（**生日問題**）：

$$\Pr[\text{在 } t = \mathrm{poly}(n) \text{ 次取樣中出現碰撞}] \;\le\; \frac{t^2}{2^n} \;=\; \mathrm{negl}(n)$$

**碰撞問題解決了。**

**為什麼不行：$$\textbf{Alice 和 Bob 不是多項式時間的了。}$$**

沒有人能真的把 $2^n$ 個 bit 算出來、存起來。

**影片裡的對話（L7 [27:39]–[28:53]）** 講得很好：

> 「用這個流程加密 $q$ 則訊息，同一個位置被用到兩次的機率是多少？」
> 學生：「$q^2 / 2^n$。」
> 「對，這叫**生日問題**。任兩個位置相同的機率是 $1/2^n$，一共有 $\binom{q}{2} \approx q^2$ 對。$q^2$ 是多項式，$2^n$ 是指數 —— 沒問題。**這就是它的美妙之處：如果我存的是一張長度 $L$ 的表，那我在用到 $\sqrt{L}$ 次的時候就會出事。**」
>
> 然後：「那為什麼還是不行？**因為要存這張巨大的表。** 我還不如直接把那一大堆 bits 存起來當金鑰算了。」

### 診斷：我們真正想要什麼（p38）

> **目標：永遠不要真的把那條指數長的字串算出來。**
>
> 我們要一個函數 $f_k(x) = b_x$ —— 那條「隱式定義的」偽隨機字串的**第 $x$ 個 bit**。
>
> - 可以在 $\mathrm{poly}(|x|) = \mathrm{poly}(n)$ 時間內算出來。
> - $f_k(x_1), f_k(x_2), \dots$ 對隨機的（或**任何相異的**）$x_1, x_2, \dots$ 而言，都與真隨機 bits **computationally indistinguishable**。
>
> 其中 $|x| = n$ 是字串 $x$ 的長度。

> 💡 **關鍵轉換：從「一條字串」變成「一個函數」。** 字串要整條算出來；函數可以**隨機存取（random access）** —— 你問哪一格，我才算哪一格。這就是 lec02 p29 預告的「PRF：擴張量指數級、而且可以隨機存取輸出的 PRG」。

---

## 6. Pseudorandom Functions (PRF)

（投影片 p39–42）

### 定義（p40）

一族函數

$$\mathcal{F}_\ell = \big\{\, f_k : \{0,1\}^\ell \to \{0,1\}^m \,\big\}_{k \in \{0,1\}^n}$$

- 由**金鑰 $k$ 索引**。
- $n$：金鑰長度；$\ell$：輸入長度；$m$：輸出長度。
- 三個參數**互相獨立**，都是 $\mathrm{poly}(\text{security parameter}) = \mathrm{poly}(n)$。
- $\mathcal{F}_\ell$ 裡的函數個數 $\le 2^n$ —— **單指數（singly exponential in $n$）**。

兩個演算法：

- **$\mathrm{Gen}(1^n)$**：隨機產生 $n$-bit 金鑰 $k$。
- **$\mathrm{Eval}(k, x)$**：多項式時間演算法，輸出 $f_k(x)$。

### 對照組：所有函數（p41）

$$ALL_\ell = \big\{\, f : \{0,1\}^\ell \to \{0,1\}^m \,\big\}$$

函數個數 $\le 2^{m \cdot 2^\ell}$ —— **雙指數（doubly exponential in $\ell$）**。

> 💡 **這個數量差距是整個概念的核心。** $\mathcal{F}_\ell$ 只有 $2^n$ 個函數，$ALL_\ell$ 有 $2^{m \cdot 2^\ell}$ 個。$\mathcal{F}_\ell$ 在 $ALL_\ell$ 裡**渺小到幾乎不存在**。
>
> 然而我們要求：**多項式時間的人分不出來。** 這就是 PRF 的膽識所在。

**影片 L7 [33:08] 的算法**：從 $\ell$ bits 到 $m$ bits 的函數，每個輸入各自可以對到 $2^m$ 種輸出，輸入有 $2^\ell$ 個，所以總數是 $(2^m)^{2^\ell} = 2^{m \cdot 2^\ell}$。而我們的家族只由 $n$-bit 金鑰索引，所以最多 $2^n$ 個。

### 安全定義（p42）

兩個世界：

| 偽隨機世界 | 真隨機世界 |
|---|---|
| $f \leftarrow \mathcal{F}_\ell$（隨機挑金鑰） | $f \leftarrow ALL_\ell$（真的隨機挑一個函數） |

Distinguisher $D$ **不是拿到一個字串，而是拿到 $f$ 的 oracle access（預言機存取）** —— 它可以送 $x$ 進去、拿 $f(x)$ 回來，想問幾次問幾次（多項式次）。最後輸出 $0/1$。

> 對所有 ppt $D$，存在 negligible $\mu$：
> $$\Big|\Pr[f \leftarrow \mathcal{F}_\ell : D^{f}(1^n) = 1] - \Pr[f \leftarrow ALL_\ell : D^{f}(1^n) = 1]\Big| \;\le\; \mu(n)$$

**什麼是 oracle access（影片 L7 [56:51]）**：

> 「他不斷問問題。他期待每次拿回來的都是**同一個函數**的值 —— 只是在不同的點上求值。現在我來玩這個遊戲：我可以用**從那個家族裡隨機挑的函數**來回答（那是我該做的），也可以用**一個完全隨機的函數**來回答。保證是：他分不出這兩種情況。」

> 💡 **這是本課第一個「互動式」的安全定義。** 之前的 distinguisher 都是拿到一個字串就結束；這裡 $D$ 可以**適應性地**（看了前面的回答再決定下一個問什麼）發問。之後的 MAC、簽章、CCA 安全都是這種形式。

---

## 7. PRF ⟹ Stateless Secret-key Encryption

（投影片 p43）

### 方案

- **$\mathrm{Gen}(1^n)$**：產生隨機 $n$-bit 金鑰 $k$，它定義了 $f_k : \{0,1\}^\ell \to \{0,1\}^m$。
  （**定義域大小 $2^\ell$ 最好是 $n$ 的超多項式（super-polynomially large）** —— 理由見下。）
- **$\mathrm{Enc}(k, m)$**：隨機挑一個 $x$，密文是那一對
  $$c = \big(\, x, \;\; y = f_k(x) \oplus m \,\big)$$
- **$\mathrm{Dec}(k, c = (x,y))$**：輸出 $f_k(x) \oplus y$。

**Correctness**：$f_k(x) \oplus y = f_k(x) \oplus f_k(x) \oplus m = m$ ✓

### 這正好修好了兩個壞主意

- **不需要狀態**：$x$ 寫在密文裡，Bob 照著算 $f_k(x)$ 就好。Alice 什麼都不用記，只要有 $k$。
- **不用算出指數長的字串**：$f_k(x)$ 是隨用隨算，$\mathrm{poly}(n)$ 時間。
- **碰撞機率 negligible**：這就是為什麼**定義域要超多項式大**。若 $2^\ell$ 只有多項式大，$\Pr[\text{碰撞}] \approx t^2/2^\ell$ 就不是 negligible，壞主意 #1 的問題會回來。

> 💡 **PRF 讓「壞主意 #2」在計算上變得可行** —— 那條指數長的偽隨機字串現在只是**隱式存在**，我們只在需要的位置把它算出來。

---

## 下一講（p44）

> **Theorem (next lec): 若存在 PRG，則存在 PRF。**（GGM 建構）

---

## 名詞對照表

| 英文 | 中文 | 說明 |
|---|---|---|
| next-bit unpredictability (NBU) | 下一位元不可預測性 | PRG 的定義 2 |
| next-bit predictor | 下一位元預測器 | 從前綴猜下一個 bit 的演算法 |
| previous-bit unpredictability | 前一位元不可預測性 | p24 的練習，同樣等價 |
| hybrid argument | 混合論證 | 把大差距切成一串小差距 |
| hybrid distribution | 混合分布 | $H_0, H_1, \dots, H_m$ |
| telescoping | 望遠鏡（伸縮）展開 | $p_m - p_0 = \sum (p_i - p_{i-1})$ |
| triangle inequality | 三角不等式 | 課堂上用來稱呼這個論證 |
| averaging argument | 平均原理 | $m$ 項和 $\ge \varepsilon$ ⟹ 有一項 $\ge \varepsilon/m$ |
| length extension | 長度擴張 | 一個 bit 的 PRG 造出多 bits 的 PRG |
| stream cipher | 串流加密法 | length extension 建構的實務名稱 |
| stateful | 有狀態的 | 雙方要記住並同步更新狀態 |
| stateless | 無狀態的 | 只需要金鑰 |
| synchrony | 同步 | stateful 方案的致命需求 |
| collision | 碰撞 | 兩次挑到同一個 pad 位置 |
| birthday problem | 生日問題 | 碰撞機率 $\approx t^2 / 2^n$ |
| pseudorandom function (PRF) | 偽隨機函數 | 可隨機存取的「指數長偽隨機字串」 |
| oracle access | 預言機存取 | 可以問函數值，但看不到函數本身 |
| singly / doubly exponential | 單指數 / 雙指數 | $2^n$ vs $2^{m \cdot 2^\ell}$ |
| random access | 隨機存取 | 問哪一格才算哪一格 |
| adaptive | 適應性的 | 看了前面的回答再決定下一個問題 |

---

## 📎 外部補充（非課堂內容）

> 以下不在投影片、也不在 L6 / L7 影片裡，是我額外加的。

**1. 為什麼 hybrid argument 的損失是「除以 $m$」**
每次用 hybrid argument，優勢會被稀釋成 $\varepsilon/m$（$m$ 是 hybrid 的個數）。這在密碼學裡是可接受的，**正因為 negligible 對乘以多項式封閉**（lec02 的 PS1 那題）：$m$ 是多項式，所以「negligible 乘 $m$」仍是 negligible，「$1/\mathrm{poly}$ 除以 $m$」仍是 $1/\mathrm{poly}$。**lec02 那題不是無聊的練習，它是這裡能成立的理由。**

**2. 第 2 節方向 2 的證明有個隱含前提**
Predictor $P$ 需要知道**哪一個** $i$ 是「好的那個 $i$」，但 Lemma 只保證存在、沒說是哪一個。標準補法：讓 $P$ **隨機猜一個 $i$**，再損失一個 $1/m$ 因子（仍是多項式）。投影片沒有明講這一步。

**3. 生日問題的 $\sqrt{\cdot}$ 直覺**
$t^2/2^n$ 這個式子的意思是：**碰撞會在大約 $\sqrt{2^n} = 2^{n/2}$ 次取樣時開始出現**，不是 $2^n$ 次。這就是影片裡那句「存一張長度 $L$ 的表，用到 $\sqrt{L}$ 次就出事」。這個 $\sqrt{\cdot}$ 之後在 collision-resistant hash functions（lec12）會再出現一次，而且是那裡的核心。

**4. 為什麼 PRF 的定義要用 oracle 而不是「給幾個 $(x, f(x))$ 對」**
Oracle 版本嚴格更強：對手可以**適應性地**選下一個要問的 $x$（看了前面的答案再決定）。投影片 p38 那句「for random (**or any distinct**) $x_1, x_2, \dots$」其實已經暗示了這件事。

**5. 延伸閱讀**
- Katz–Lindell，3.3 節（PRG 的 length extension）、3.5 節（PRF）
- Boneh–Shoup（在 `books/`），第 3 章（stream ciphers）、第 4 章（PRF）
- Goldreich，*Foundations of Cryptography* Vol. 1，3.2–3.6 節（hybrid argument 的標準處理）

---

## ⚠️ 存疑處

| 位置 | 問題 |
|---|---|
| 投影片 p19–21 | 這三頁是**動畫疊印**的，PDF 文字層把好幾個版本的文字混在一起（例如 p19 的 “∃i such that D distinguishes…” 和 “D distinguishes between Hm and H0…” 疊在一起）。我按數學邏輯重建了 hybrid 的定義與推導，**請對照原始 PDF 的圖確認**。 |
| 投影片 p17 vs p23 | p17 把優勢定義成 $\varepsilon := 1/p'(n)$，但 p23 最後寫的是 $1/(m \cdot p(n))$（用 $p$ 而非 $p'$）。**投影片自己的符號不一致**，指的是同一個東西。 |
| 投影片 p21 | 這頁疊印最嚴重，`Claim`、`Corollary`、`Define` 幾行互相插在一起。我判讀為：Claim 是 $p_{i-1} = (p_i + \tilde{p_i})/2$，Corollary (\*) 是 $p_i - \tilde{p_i} \ge 2\varepsilon/m$。 |
| 投影片 p31 | length extension 的**安全性證明留作練習**，投影片沒有寫。本筆記只記了提示。 |
| 投影片 p38 | 標題文字層是 `ButPseudorandom` / `these are goodFunctions bad ideas…` 兩層疊印。正確應為標題「Pseudorandom Functions」+ 上一頁殘留的「But these are good bad ideas…」。 |
| 投影片 p40–43 | 下標在文字層裡壞掉（`{0,1}!`、`ℱℓ`、`𝑓8`、`2&` 之類）。我按上下文還原成 $\mathcal{F}_\ell$、$f_k$、$2^n$ 等，**公式請對照原 PDF 的圖**。 |
| L7 字幕品質 | L7 用的是舊版自動字幕，沒有標點、人名與術語大量錯誤（例如生日問題被聽成 “the budget problem”、pseudorandom functions 被聽成 “pseudo random process”）。所有數學內容都已用投影片校正。 |
| L7 後半 | L7 從大約 [53:21] 之後進入 **GGM 樹狀建構（PRG ⟹ PRF）**，那是 Fall 2022 的 **lec04**（投影片 p44 明講 “next lec”）。依 BRIEF 的規則**沒有寫進本筆記**。 |
