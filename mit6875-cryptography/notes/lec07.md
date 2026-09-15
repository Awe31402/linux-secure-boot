# Lecture 7 — Goldreich–Levin：真正的證明

> **來源說明**
> - 投影片：`slides/lec07.pdf`（**Fall 2022**，24 頁，有完整文字層）—— **主要來源**。
> - 影片：2018 那套的 **L5「Hardcore Bits II」**（<https://youtu.be/UuQuF0tcn1E>）。
>   YouTube 字幕是舊版（沒標點），**已自行用 Whisper 轉錄**。
>
> **⚠️ `README.md` 的課程索引對這一堂是錯的。**
>
> 索引寫 lec07 是「Goldreich–Levin (contd.); local list decoding; **primes and $\mathbb{Z}_p^*$; discrete log**」。
> 但實際投影片**完全沒有數論** —— 24 頁裡有 19 頁在講 GL，最後幾頁是兩個猜想和課程地圖。
> 質數與 discrete log 應該在 **lec08**（它的索引寫著「group & number theory overview」）。
>
> **本堂的影片對應很乾淨**：L5 幾乎整堂都在講這件事。
>
> | lec07 投影片 | L5 |
> |---|---|
> | p7–11 回顧 L6 的弱版證明、找出兇手 | ✅ |
> | p12–17 真正的證明（parsimony、Chebyshev） | ✅ `[45:22]`–`[54:42]` |
> | p18–19 編碼理論視角、list decoding | ✅ `[59:08]`–`[60:15]` |
> | p21–22 兩個猜想 | ❌ 沒有（那是 Fall 2022 講者自己的猜想） |
>
> ⚠️ Whisper 把 **Goldreich–Levin 聽成 “Goldrick Levin”、Chernoff 聽成 “Chernobyl”**。數學內容以投影片為準。
>
> 標 `📎 補充` 的區塊不是課堂內容，是我額外加的。

---

## 一句話總結

**lec06 的證明卡在 $\frac34$，因為 union bound 把誤差乘了兩倍** —— 真正的證明只問 predictor **一次**（另一半自己猜），再用 **pairwise independence** 讓「自己猜」的代價從 $2^n$ 掉到 $m$，於是門檻一路壓到 $\frac12$。

---

## 1. GL 定理的兩個版本

（投影片 p3–p5）

投影片開頭把 lec06 那句口號**修正**了一下：

> ~~Goldreich–Levin Theorem: “every OWF has a HCB.”~~
>
> **Goldreich–Levin Theorem：對每個 OWF/OWP $F$，存在另一個 OWF/OWP $F'$，它有一個 HCB。**

這個修正很重要 —— 嚴格來說 GL 給的不是「$F$ 自己的」hardcore bit，而是一個**改造過的** $F'$ 的。

### Version 1（p4）：隨機的 predicate

定義一族 predicate，每個 $r$ 一個：

$$B_r(x) = \langle r, x \rangle = \sum_{i=1}^{n} r_i x_i \bmod 2$$

> 對每個 one-way function $F$、每個 PPT $A$，存在 negligible $\mu$：
> $$\Pr\big[x \leftarrow \{0,1\}^n;\, r \leftarrow \{0,1\}^n \;:\; A(F(x), r) = B_r(x)\big] \;\le\; \frac{1}{2} + \mu(n)$$

**隨機挑的 $B_r$ 對每個 OWF 都是 hardcore 的。**

### Version 2（p5）：確定性的 predicate

> 對每個 one-way function / permutation $F$，存在一個相關的
> $$F'(x, r) = \big(F(x),\, r\big)$$
> 它有一個**確定性的** hardcore predicate，具體來說就是
> $$B(x, r) = \langle r, x \rangle \bmod 2$$

**把隨機性 $r$ 吸收進函數的輸入裡。** $F'$ 仍然是 OWF（要反轉它還是得反轉 $F$），而且如果 $F$ 是 permutation，$F'$ 也是。

> **Key Point：這個版本足以從任何 OWP 造出 PRG。**

---

## 2. OWP ⇒ PRG（完整版）

（投影片 p6）

lec06 寫的是 $G(x) = F(x) \| B(x)$，但當時 $B$ 還是個「假設存在」的東西。現在用 GL Version 2 把它填實：

$$\boxed{\;G(x, r) \;=\; F'(x,r) \,\big\|\, \langle r, x\rangle \;=\; F(x) \,\big\|\, r \,\big\|\, \langle r, x \rangle\;}$$

> **Theorem：假設 $F$ 是 one-way permutation，則 $G$ 是 PRG。**

**輸入 $2n$ bits（$x$ 和 $r$），輸出 $2n + 1$ bits。** 拉長一個 bit —— 再配上 lec03 的 length extension，就能拉到任意多項式長度。

> 💡 **注意 $r$ 被原封不動地輸出了。** 這看起來很浪費，但正是關鍵：
> $F$ 是排列所以 $F(x)$ 均勻，$r$ 本來就均勻，**所以前 $2n$ 個 bit 是真正均勻的**。
> 唯一「需要偽隨機」的只有最後那一個 bit，而那正是 hardcore predicate 保證的。

---

## 3. 回顧：L6 證的是弱版

（投影片 p7–10）

lec06 假設的是一個**相當好**的 predictor：

$$\Pr\big[x, r \;:\; P(F(x), r) = \langle r, x\rangle\big] \;\ge\; \mathbf{\frac{3}{4}} + \frac{1}{p(n)}$$

證明分三步（細節見 lec06 筆記）：

1. **Averaging argument**：至少 $\frac{1}{2p(n)}$ 比例的 $x$ 是 **good $x$**，滿足
   $$\Pr_r\big[P(F(x), r) = \langle r, x\rangle\big] \ge \frac34 + \frac{1}{2p(n)}$$
   （投影片 p8 註明 **“Proof: On the board.”** —— 沒寫在投影片上。）

2. **Linearity**：挑隨機 $r$，問 $P$ 兩次（$\langle r,x\rangle$ 和 $\langle r \oplus e_i, x\rangle$），XOR 得到 $x_i$。

3. **Majority**：重複 $O(\log n \cdot p(n)^2)$ 次取多數決，Chernoff + union bound 收尾。

---

## 4. 兇手是誰？

（投影片 p11）

**這一頁是整堂課的樞紐。** 投影片把第 2 步的算式再抄了一次，然後把其中一行**粗體標出來**：

$$
\begin{aligned}
\Pr[\text{算對 } x_i]
&\ge 1 - \Big(\mathbf{\Pr[P \text{ 對 } \langle r,x\rangle \text{ 答錯}]} + \mathbf{\Pr[P \text{ 對 } \langle r \oplus e_i, x\rangle \text{ 答錯}]}\Big) \\
&\ge 1 - 2\left[\frac14 - \frac{1}{2p(n)}\right] = \frac12 + \frac{1}{p(n)}
\end{aligned}
$$

> **兇手就是那個 $\times 2$。**

因為我們**問了 $P$ 兩次**，union bound 就把錯誤率乘了兩倍。於是：

- 要讓 $1 - 2 \cdot (\text{錯誤率})$ 大於 $\frac12$，錯誤率必須 $< \frac14$ —— 這就是 $\frac34$ 這個門檻的來源。
- 如果 predictor 只有 $\frac12 + \varepsilon$，錯誤率接近 $\frac12$，那 $1 - 2 \cdot \frac12 = 0$。**什麼都保證不了。**

> 💡 **診斷清楚了，解法也就浮現了：想辦法只問 $P$ 一次。**

---

## 5. 真正的證明

（投影片 p12–17，歸功於 **Charlie Rackoff**）

現在只假設（averaging 之後）至少 $\frac{1}{2p(n)}$ 比例的 $x$ 滿足

$$\Pr_r\big[P(F(x), r) = \langle r, x\rangle\big] \;\ge\; \mathbf{\frac{1}{2}} + \frac{1}{2p(n)}$$

### 第一步：假裝有人幫忙（p12）

> **先假設我們有一點「建議 / 幫助」。**

挑一個隨機 $r$，**向一個 Oracle 要 $\langle r, x\rangle$**，只**向 $P$ 要 $\langle r \oplus e_i, x\rangle$**。兩個相減得到 $x_i$。

$$\Pr[\text{算對 } x_i] \;\ge\; \Pr\big[P \text{ 對 } \langle r \oplus e_i, x\rangle \text{ 答對}\big] \;\ge\; \frac12 + \frac{1}{2p(n)}$$

**沒有 union bound，沒有 $\times 2$。** 門檻直接降到 $\frac12$。

### 第二步：把 Oracle 換成「自己猜」（p13）

Oracle 當然不存在。那就**自己猜** $\langle r, x\rangle$ —— 反正它只是一個 bit。

> 如果我們的猜測**全部正確**，那分析就跟前面一模一樣。
>
> **但那個機率有多大⋯⋯？**

需要的 $r$ 有

$$m = O\big(n \log n \cdot p(n)^2\big)$$

個。全部猜對的機率是 $2^{-m}$ —— **荒謬地小**。

**課堂上的說法（L5 [45:22]）**：這等於在直接猜 $x$，完全沒有意義。

### 第三步：Parsimony in Guessing（節省地猜）（p14）

**關鍵的轉念：不要猜 $m$ 個，只猜 $\log(m+1)$ 個。**

1. 挑 $\log(m+1)$ 個**隨機種子向量** $s_1, \dots, s_{\log(m+1)}$。
2. **猜** $c_j = \langle s_j, x\rangle$（每個都是一個 bit）。

   全部猜對的機率是
   $$\frac{1}{2^{\log(m+1)}} = \frac{1}{m+1}$$
   投影片的評語：**“which is not bad.”**（$m$ 是多項式，所以 $\frac{1}{m+1}$ 也是多項式的倒數。）

3. **從種子生出所有需要的 $r$**：令 $T_1, \dots, T_m$ 是 $\{1, 2, \dots, \log(m+1)\}$ 的所有**非空子集合**，定義

   $$r_i = \bigoplus_{j \in T_i} s_j \qquad\text{和}\qquad b_i = \bigoplus_{j \in T_i} c_j$$

> **Key Observation：若 $c_1, \dots, c_{\log(m+1)}$ 全部正確，則 $b_1, \dots, b_m$ 也全部正確。**

**為什麼**（內積的雙線性）：

$$\langle r_i, x\rangle = \Big\langle \bigoplus_{j \in T_i} s_j,\; x \Big\rangle = \bigoplus_{j \in T_i} \langle s_j, x\rangle = \bigoplus_{j \in T_i} c_j = b_i$$

> 💡 **這就是全部的魔術**：猜對 $\log(m+1)$ 個 bit，就**免費得到** $m$ 個 $r$ 的內積值。
> 非空子集合有 $2^{\log(m+1)} - 1 = m$ 個 —— 數字剛好對上。

**而且還有一個附帶好處（p17）**：既然只有 $2^{\log(m+1)} = m+1$ 種可能的猜法，**你甚至可以全部枚舉一遍**。

### 第四步：反轉器（p15）

```
OWF Inverter A：
  產生隨機種子 s₁, …, s_{log(m+1)} 和猜測位元 c₁, …, c_{log(m+1)}
  由它們導出 r₁, …, r_m 和 b₁, …, b_m

  對每個 i ∈ {1, 2, …, n}：
      重複 100·n·p(n)² 次（每次用一個不同的 rⱼ）：
          向 P 要 ⟨rⱼ ⊕ eᵢ, x⟩
          把回答和 bⱼ 做 XOR，得到 xᵢ 的一個猜測
      對所有猜測取多數決，定下 xᵢ
  輸出所有 xᵢ 串起來的 x
```

**注意：每一輪只問 $P$ 一次。** 另一半來自 $b_j$（我們自己算的）。

### 第五步：分析（p16）

先**條件在「所有 $c_j$ 都猜對」**這個事件上。

> **主要的麻煩：這些 $r_i$ 彼此不獨立** —— 它們都是同一批種子的組合。**所以不能用 Chernoff。**
>
> **Key Observation：這些 $r_i$ 是 pairwise independent（兩兩獨立）的。**
> **因此可以用 Chebyshev！**

**為什麼兩兩獨立（L5 [52:59]–[53:21]）**：

取兩個不同的子集合，例如 $T = \{1,2\}$ 和 $T' = \{2,3\}$。它們重疊得很厲害，但：

- $r_T = s_1 \oplus s_2$ —— 兩個隨機向量的和，是隨機的。
- **條件在 $r_T$ 之下看 $r_{T'} = s_2 \oplus s_3$**：$s_2$ 已經被用掉了（固定了），
  但 **$s_3$ 還沒被用過，它把整個東西重新隨機化。**

一般情況：只要兩個子集合**不相同**，就一定有一個下標只屬於其中一邊 —— 那個種子就負責隨機化。

> ⚠️ **但三個以上就不獨立了**：例如 $r_{\{1\}} \oplus r_{\{2\}} \oplus r_{\{1,2\}} = 0$，永遠成立。

結論：

$$p \;:=\; \Pr[\text{Inverter 成功} \mid \text{所有猜測正確},\, \text{good } x] \;\ge\; 0.99$$

（投影片註明證明在黑板上。）

> 📎 **Chebyshev 的代價**：Chernoff 需要完全獨立，能給出指數級的集中；Chebyshev 只需要兩兩獨立，
> 但收斂慢得多 —— 需要的樣本數從 $O(\log n)$ 變成 $O(p(n)^2)$。
> **課堂上的評語（L5 [47:43]）**：「$p(n)^2$ 和 $p(n)^2 \cdot n^2$ 之間有差嗎？**一個多項式跟另一個多項式，都一樣。**」

### 第六步：全部乘起來（p17）

$$
\begin{aligned}
\Pr[\text{Inverter 成功}]
&\ge \Pr[\text{成功} \mid \text{猜測全對},\, \text{good } x] \cdot \Pr[\text{猜測全對}] \cdot \Pr[\text{good } x] \\[4pt]
&= p \cdot \underbrace{\frac{1}{m+1}}_{\text{parsimony}} \cdot \underbrace{\frac{1}{2p(n)}}_{\text{averaging}}
\end{aligned}
$$

三個因子**都是多項式的倒數**，乘起來仍然是多項式的倒數。而 $p \ge 0.99$，所以整體成功率是 $\frac{1}{\mathrm{poly}(n)}$ —— **不是 negligible，與 $F$ 是 OWF 矛盾。** $\blacksquare$

**還可以更好（p17）**：

> 也可以把成功率提高到約 $\frac{1}{p(n)}$ —— **把所有的「猜測」枚舉一遍**。
> 每一組猜測會給出一個「宣稱的反像」，而**我們可以檢查哪一個才是真的反像！**

**為什麼檢查很便宜**：$F$ 是**容易計算**的。拿到候選 $x'$，算一下 $F(x')$ 看等不等於 $y$ 就好。

> 💡 **這是整個證明的收尾，也是它能運作的理由**：
> 我們不需要「一次就猜對」，只需要**產生一份不太長的候選清單**，再用 $F$ 把假的濾掉。

---

## 6. 編碼理論的視角

（投影片 p18）

把映射

$$x \;\longmapsto\; \big(\langle x, r\rangle\big)_{r \in \{0,1\}^n}$$

看成 $x$ 的編碼：$n$ bits 變成 $2^n$ bits，**極度冗餘、指數長**。這就是 **Hadamard code**。

而 $P(F(x), \cdot)$ 相當於：**提供一個「有雜訊的碼字」的存取管道**。

於是這兩堂課證的東西可以翻譯成：

| | 相當於 |
|---|---|
| **lec06 的弱版** | Hadamard code 的 **unique decoding**，容錯率 $\frac14 - \frac{1}{p(n)}$ |
| **本堂的真正證明** | Hadamard code 的 **list-decoding**，容錯率 $\frac12 - \frac{1}{p(n)}$ |

**課堂上的說法（L5 [59:40]–[60:15]）**：

> Goldreich–Levin 的核心就是一個 **list decoding 演算法**。
> 這個碼把 $n$ bits 展開成 $2^n$ bits —— 從碼率的角度看**糟透了**。
> **但它的糾錯能力極好**：就算對手破壞了「一半再少一點點」的位元，你還是救得回來。
>
> 而且 **list decoding 這個領域，某種程度上就是從密碼學這裡長出來的。**

> 📎 **為什麼 $\frac12$ 一定要用 list decoding**：雜訊率接近 $\frac12$ 時，**唯一解碼在資訊理論上就不可能** ——
> 可能有好幾個碼字同樣接近你手上這串雜訊，沒有任何演算法能分辨。
> 所以只能吐出**清單**。這正好對應到第五步末尾那個「枚舉猜測再用 $F$ 過濾」。

---

## 7. 推廣：從任何 list-decodable code 造 hardcore predicate

（投影片 p19，歸功於 **Impagliazzo 和 Sudan**）

上一節的對應不是巧合，而是一個**通用的配方**：

設 $x \mapsto C(x)$ 是某個編碼。

> 給定一個在 $\frac12 - \varepsilon$ 比例的位置上出錯的 $C(x)$，list-decoder 會輸出一份候選清單 $\{x_1, \dots, x_m\}$。
>
> **那麼 hardcore predicate 就是**
> $$B_i(x) = C(x)_i$$
> （也就是「碼字的第 $i$ 個位元」。）

**為什麼成立**：

1. 一個 hardcore-bit predictor **就等於**給了我們一個**被破壞的碼字**的存取管道。
2. 在它上面跑 **list-decoder**，得到一份可能的反像清單。
3. **因為 OWF 容易計算**，我們可以把假的反像**過濾掉**。

> 💡 **GL 只是這個配方套用在 Hadamard code 上的特例。** 換一個 list-decodable code，就得到另一個 hardcore predicate。

---

## 8. 兩個開放猜想

（投影片 p21–22）

GL 給的是「**隨機的** $B_r$ 是 hardcore」。那能不能對每個 $F$ 找到一個**固定的**、確定性的 hardcore predicate？

### Conjecture 1（非均勻版）

> 對每個 one-way function $F$，**存在**一個電路 $B_F$，使得對每個 PPT 對手 $A$，存在 negligible $\mu$：
> $$\Pr\big[x \leftarrow \{0,1\}^n \;:\; A(F(x)) = B_F(x)\big] \;\le\; \frac12 + \mu(n)$$

投影片作者還加了一個更強的版本：

> 事實上，**我猜想**對每個 one-way function $F$，都存在某個 $r_F$，使得
> $B_{r_F}(x) = \langle r_F, x\rangle$ 是 hardcore 的。

### Conjecture 2（可有效產生版）

> 同上，但要求 $B_F$ 是一個 **efficiently generatable（可有效產生的）**電路。

**兩者的差別**：Conjecture 1 只說那個電路**存在**（non-uniform —— 對每個 $n$ 可以有不同的「建議」，而且不保證找得到）。Conjecture 2 要求我們**真的能算出它來**。

> 💡 這就是 lec06 提到的「我最喜歡的開放問題：把 non-uniformity 拿掉」的正式版本。
> **注意 lec06 p23 說「universal hardcore predicate 不存在」（PS2），與這裡不矛盾** ——
> 那裡問的是「**一個** predicate 對**所有** $F$ 都有效」，這裡問的是「**每個** $F$ 各自有**一個**」。
> 量詞的順序不同。

---

## 9. Recap 與課程地圖

（投影片 p20, p23–24）

### 這兩堂做完的事

1. 定義了 **one-way functions (OWF)**
2. 定義了 **hardcore bits (HCB)**
3. **Goldreich–Levin 定理**：每個 OWF 都有一個 HCB
4. 證明了 **one-way permutations ⇒ PRG**
   （事實上 **OWF ⇒ PRG** 也成立，但那是困難得多的定理）

### 之後可能會講的（p23，“Time permitting”）

1. **OWF ⇒ PRG？**
2. **從 PRF 造 Pseudorandom Permutations** —— **Luby–Rackoff 建構**

### Minicrypt 地圖（p24）

跟 lec06 p2 同一張圖，但底下多了一行：

```
                              OWF
                               ▲
        Candidate Constructions: from number theory,
                geometry, combinatorics, …
```

> 💡 **地基補完了。** 前六堂蓋的所有東西（PRG、PRF、加密、MAC、CCA 安全⋯⋯）
> 現在全部掛在 OWF 這一個假設上，**而且那條線是真的接起來的**：
> OWF → (GL) → hardcore bit → PRG → PRF → 其餘一切。
>
> 剩下的問題只有一個：**OWF 的候選從哪來？** 答案是數論、幾何、組合數學 —— 那是 lec08 之後的事。

---

## 名詞對照表

| 英文 | 中文 | 說明 |
|---|---|---|
| Goldreich–Levin theorem | — | 每個 OWF 都有 hardcore bit |
| Charlie Rackoff | — | 真正證明的提出者 |
| union bound | 聯集界 | 本堂的「兇手」 |
| oracle / advice | 預言機 / 建議 | 第一步的虛構幫手 |
| parsimony in guessing | 節省地猜 | 只猜 $\log(m+1)$ 個而非 $m$ 個 |
| seed vector | 種子向量 | $s_1, \dots, s_{\log(m+1)}$ |
| bilinearity | 雙線性 | $\langle \oplus s_j, x\rangle = \oplus \langle s_j, x\rangle$ |
| pairwise independence | 兩兩獨立 | 任兩個獨立，三個以上未必 |
| Chernoff bound | — | 需完全獨立，收斂快 |
| Chebyshev inequality | 柴比雪夫不等式 | 只需兩兩獨立，收斂慢 |
| averaging argument | 平均論證 | 導出 good $x$ |
| good $x$ | — | predictor 在其上表現特別好的那些 $x$ |
| Hadamard code | 阿達馬碼 | $n$ bits → $2^n$ bits |
| unique decoding | 唯一解碼 | 容錯率 $< \frac14$ |
| list decoding | 列表解碼 | 容錯率接近 $\frac12$，輸出候選清單 |
| list-decodable code | 可列表解碼的碼 | Impagliazzo–Sudan 配方的輸入 |
| non-uniform | 非均勻 | 每個 $n$ 可有不同「建議」，不保證找得到 |
| efficiently generatable | 可有效產生的 | 真的算得出來 |
| Luby–Rackoff | — | 從 PRF 造 PRP 的建構 |

---

## 📎 外部補充（非課堂內容）

> 以下不在投影片、也不在 L5 影片裡，是我額外加的。

**1. 為什麼 $m = O(n \log n \cdot p(n)^2)$**
反轉器要定 $n$ 個位元，每個位元要 $O(p(n)^2)$ 次取樣（Chebyshev 的代價），再乘上 $O(\log n)$ 讓 union bound 能保證 $n$ 個位元**同時**正確。三者相乘就是 $m$。而 parsimony 只需要 $\log(m+1) = O(\log n)$ 個種子 —— **指數級的節省**。

**2. Chernoff vs Chebyshev 的具體差別**
要讓失敗機率降到 $\delta$：Chernoff 需要 $O(\varepsilon^{-2}\log\frac1\delta)$ 次取樣；Chebyshev 需要 $O(\varepsilon^{-2}\delta^{-1})$ 次。差在 $\log\frac1\delta$ 與 $\frac1\delta$ —— 指數 vs 多項式。本堂能接受，是因為我們只需要把失敗機率壓到常數（$p \ge 0.99$），不需要壓到 negligible。

**3. Hadamard code 的距離**
任兩個相異碼字的 Hamming 距離恰好是 $2^{n-1}$，也就是碼長的一半。這解釋了為什麼容錯上限就是 $\frac12$：超過一半，你就分不清是哪個碼字了。

**4. 延伸閱讀**
- Goldreich, *Foundations of Cryptography* Vol. 1，2.5.2 節（GL 的完整證明）
- Katz–Lindell，7.2 節
- Impagliazzo & Sudan 的觀點見 Sudan 的 list-decoding 綜述
- 原始論文：Goldreich & Levin, *A Hard-Core Predicate for all One-Way Functions*, STOC 1989

---

## ⚠️ 存疑處

| 位置 | 問題 |
|---|---|
| **`README.md` 的課程索引錯了** | 索引寫 lec07 含「primes and $\mathbb{Z}_p^*$; discrete log」，但**投影片完全沒有數論**。那些內容應在 lec08。做 lec08 時要注意。 |
| 投影片 p8 | averaging argument 的證明是 **“Proof: On the board.”** —— 投影片沒寫。 |
| 投影片 p16 | $p \ge 0.99$ 的證明註明「Pf. on the board, also in the next two slides」，但**接下來的兩頁並沒有那個計算**（p17 是總結，p18 是編碼視角）。**這個關鍵的 Chebyshev 計算在投影片上是缺的。** |
| 投影片 p15 | 反轉器內層迴圈寫的是 `Ask 𝑃 to tells us 𝑟# + 𝑒# , 𝑥`，兩個下標在文字層裡都變成 `#`。按語意應是 $\langle r_j \oplus e_i, x\rangle$（外層跑 $i$、內層跑 $j$）。**請對照原 PDF 的圖確認。** |
| 投影片 p9, p12, p17 | 數學下標大量損壞（`≥1−2T ( − )* "`、`= ) + 1/𝑝(𝑛)`、`)" * " *`）。我按上下文還原，算式是通的，但**公式請對照原圖**。 |
| 投影片 p21–22 | 兩個猜想是 **Fall 2022 講者自己的**，2018 的影片裡沒有。我只照投影片寫，沒有額外詮釋。 |
| L5 字幕 | 自轉的 Whisper 稿，人名仍有錯：**Goldreich–Levin → “Goldrick Levin”、Chernoff → “Chernobyl”**。數學內容以投影片為準。 |
| 本堂與 lec06 的重疊 | p7–p11 是 lec06 內容的複習（而且 p20 的 Recap 與 lec06 p33 一字不差）。本筆記把它壓縮成第 3 節，重點放在 p11「兇手是誰」這個新的診斷上。 |
