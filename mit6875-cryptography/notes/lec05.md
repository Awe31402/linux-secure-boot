# Lecture 5 — Identification, MACs (EUF-CMA), IND-CCA2

> **來源說明**
> - 投影片：`slides/lec05.pdf`（**Fall 2022**，33 頁，有完整文字層）—— **主要來源**。
> - 影片：2018 那套的 **L15「Message Authentication Codes, Digital Signatures」**（<https://youtu.be/Kp2JqEuoTuI>）。字幕是舊版差品質（無標點、術語大量錯誤）。
>
> **⚠️ 影片只涵蓋本堂的一部分。** 我也檢查了 L16，它整堂都在講數位簽章與碰撞阻抗（= Fall 2022 的 lec11–12），沒有補到缺口。
>
> | lec05 投影片 | 有沒有影片 |
> |---|---|
> | p3–6 friend-or-foe 辨識、challenge-response | ❌ **沒有** |
> | p8–9 學習理論（Kearns–Valiant） | ❌ **沒有** |
> | p11–22 MAC 定義、EUF-CMA、加密 ≠ 認證、replay | ✅ L15 有，對得不錯 |
> | p23–28 長訊息的 MAC、hash-then-sign | △ L15 尾端帶到，但很快轉往簽章 |
> | p30–33 IND-CCA2 | ❌ **沒有** |
>
> 好消息是這份投影片本身寫得很完整（不像 lec04 是手寫的），缺影片影響不大。
>
> ---
>
> ### 符號提醒：本堂回到 **lec03** 的慣例
>
> | | 輸入長度 | 輸出長度 | 安全參數 |
> |---|---|---|---|
> | lec03、**lec05（本篇）** | $\ell$ | $m$ | $n$ |
> | lec04（手寫講義） | $m$ | $n$ | $\lambda$ |
>
> 也就是說，**lec04 是特例**，lec05 又切回去了。讀的時候注意。
>
> ---
>
> 標 `📎 補充` 的區塊不是課堂內容，是我額外加的。

---

## 一句話總結

**加密保護的是「別人看不懂」，完全不保護「別人改不了」** —— 這兩件事是不同的目標，需要不同的工具（MAC），而把兩者正確地黏起來（Encrypt-then-MAC）才能擋住能操弄密文的對手（IND-CCA2）。

---

## 這堂要回答什麼

副標題其實是：**PRF 的更多應用**。四個：

1. **識別協定（Identification Protocols）** —— 怎麼證明「我是我」
2. **學習理論的應用** —— 一個意外的副產品
3. **認證（EUF-CMA Security）** —— 怎麼確保訊息沒被竄改
4. **IND-CCA Security** —— 對手能操弄密文時的安全

---

## 1. Friend-or-Foe 識別

（投影片 p3–6）

### 問題

對手是 **person-in-the-middle（中間人）**：可以**竊聽也可以修改**通訊，目標是**冒充**成 Tim。

### 先補一條引理：PRF 的不可預測性

（p4–5）

設 $f_k : \{0,1\}^\ell \to \{0,1\}^m$ 是 PRF。

> 考慮一個對手，她要到並取得了 $f_k(x_1), \dots, f_k(x_q)$（$q = q(n)$ 是多項式）。
>
> 她能不能預測 $f_k(x^*)$，其中 $x^*$ 由她自己選、且 $x^* \notin \{x_1, \dots, x_q\}$？她能做多好？

> **Lemma.** 若她的成功機率達到 $\dfrac{1}{2^m} + \dfrac{1}{\mathrm{poly}(n)}$，**她就打破了 PRF 安全性**。
>
> 而只要 $m$ 夠大（**即 $m = \omega(\log n)$**），$\frac{1}{2^m}$ 在 $n$ 之下就是 negligible。

**為什麼是 $1/2^m$ 而不是 $0$**：就算 $f$ 是**真正的隨機函數**，對手還是可以**亂猜** —— 猜中一個 $m$-bit 的值機率是 $1/2^m$。所以我們只能要求「不能贏過亂猜太多」。

**為什麼要 $m = \omega(\log n)$**：若 $m = O(\log n)$，則 $2^m = \mathrm{poly}(n)$，於是 $1/2^m$ 本身就是 $1/\mathrm{poly}(n)$ —— **不是 negligible**，亂猜就有實質成功率。

### 一個容易混淆的點（p5）

投影片並列了兩句話：

> - **Unpredictability ≡ Indistinguishability for bits**（lecture 3）
> - **Indistinguishability ⟹ Unpredictability**（but **not vice versa**）

乍看矛盾，其實不是：

- **輸出是單一 bit 時**：兩者**等價**。這就是 lec03 那個 NBU ⟺ Indistinguishability 定理。
- **輸出比較長時**：indistinguishability **嚴格更強**。

> 📎 **為什麼長輸出時不等價**：想像一個函數，輸出的**第一個 bit 永遠是 0**，其餘 bits 完全隨機。它**不可預測**（你猜不中整個 $m$-bit 輸出，機率仍約 $1/2^{m-1}$，跟 $1/2^m$ 只差一點點，可能還在容許範圍內），但它**極容易區分** —— 看第一個 bit 就好。
>
> 所以「猜不中整串」比「分不出來」弱。

### Challenge-Response 協定

（p6）

```
   驗證方                                      Tim
 (PRF Key s)                          (ID number ID, PRF Key s)

        ───────────  隨機 r  ───────────▶

        ◀──────── (ID, f_s(r)) ─────────
```

驗證方丟一個**隨機挑戰** $r$，Tim 用共享的 PRF 金鑰算 $f_s(r)$ 回去。驗證方自己也算一次，比對。

### 為什麼安全（投影片的 “Proof”）

> 對手蒐集了多項式多組 $(r_i, f_s(r_i))$（甚至 $r_i$ 可以由她指定）。
> 當她要冒充時，她**必須**針對一個**全新的隨機 $r^*$** 產生出 $f_s(r^*)$。
>
> 只要 PRF 的**輸入與輸出長度都夠長**（$\omega(\log n)$），這件事就是困難的。

**兩個長度為什麼都要夠長**：

- **輸出長度 $m$**：否則亂猜就中（上面那條引理）。
- **輸入長度 $\ell$**：否則新的隨機 $r^*$ 很可能**剛好就是**她之前問過的某個 $r_i$ —— 那她直接查表就好。$\ell = \omega(\log n)$ 保證碰撞機率 negligible（又是生日問題）。

---

## 2. （插曲）學習理論裡的負面結果

（投影片 p8–9）

> **Theorem [Kearns and Valiant 1994].**
> **假設 PRF 存在，則存在一些 hypothesis class 是多項式時間演算法學不會的。**

**直覺**：PRF 家族 $\{f_k\}$ 就是一個學不會的 hypothesis class。給你多項式多組 $(x_i, f_k(x_i))$ 樣本，你仍然無法預測新的點 $f_k(x^*)$ —— 那正是上面那條引理說的事。

而「能從樣本預測新的點」正是**學習**的定義。所以：**PRF 的存在，直接推出某些東西學不會。**

> 💡 **密碼學和機器學習在這裡是同一枚硬幣的兩面。**
> 密碼學要的是「看了一堆樣本還是預測不出來」；學習理論要的是「看了一堆樣本就能預測」。
> **一邊的成功就是另一邊的失敗。** lec01 提過這門課的副產品之一是 average-case vs worst-case hardness 的理解，這是另一個副產品。

> ⚠️ 投影片 p9 只有一張標題頁「Machine Learning and Cryptography (A quick aside)」，實際內容應該是課堂上口頭講的，**而這段沒有影片**。上面的直覺是我補的。

---

## 3. 認證問題

（投影片 p11–12）

### 問題

```
      m
   Alice ────── m ──────▶ 【Eve】 ────── m' ──────▶ Bob
   Key k              可以竄改、                    Key k
                      也可以注入新訊息
```

這叫 **man-in-the-middle attack**。

> **Bob 要怎麼檢查這則訊息真的是 Alice 發的？**

### 解法的形狀

```
      m
   Alice ──── (m, t) ────▶ 【Eve】 ──── (m,t) 或 ⊥ ────▶ Bob
   Key k              基本上只能                        Key k
                      原封不動轉送
```

> 我們要 Alice 為訊息 $m$ 產生一個 **tag（標籤）$t$**，而這個 tag **沒有秘密金鑰 $k$ 就很難產生**。

### 一個做不到的事（影片 L15 [3:06]）

Vinod 一開場就講清楚了期望值：

> **你沒辦法保證總是能還原出 Alice 送的訊息** —— 那不可能（Eve 可以直接把訊息**刪掉**）。
>
> **但你可以保證「偵測得出來」** —— 保證 Bob **不會接受 Alice 沒有送過的訊息**。

**這就是 authentication 的目標。** 注意它是一個**否定式**的保證。

---

## 4. Message Authentication Codes (MAC)

（投影片 p13）

三個演算法 $(\mathrm{Gen}, \mathrm{MAC}, \mathrm{Ver})$：

- **$\mathrm{Gen}(1^n)$**：產生金鑰 $k \leftarrow K$。
- **$\mathrm{MAC}(k, m)$**：輸出 tag $t$。（**可以是確定性的** —— 本堂看到的都是。）
- **$\mathrm{Ver}(k, m, t)$**：輸出 **Accept** 或 **Reject**。

**Correctness**：

$$\Pr[\mathrm{Ver}(k, m, \mathrm{MAC}(k,m)) = \text{Accept}] = 1$$

**Security（直覺）**：難以偽造。應該很難生出一組新的 $(m', t')$ 讓 $\mathrm{Ver}$ 接受。

> 💡 注意 MAC 和加密的一個結構差異：**MAC 可以是確定性的**，而 lec04 才剛證明加密**必須**是機率性的。這不矛盾 —— 兩者的安全目標不同。（但這也導致 MAC 不保護隱私，見第 7 節。）

### 對手有多強？（p14）

- 可以看到很多組 $\big(m, \mathrm{MAC}(k,m)\big)$。
- **可以存取 MAC oracle $\mathrm{MAC}(k, \cdot)$** —— 拿**自己選的**任何訊息去要 tag。

這叫 **chosen message attack (CMA)**。

> 跟 lec04 的 IND-**CPA** 是同一個精神：對手不只被動看，還能主動點餐。

### 「打破」有三種強度（p15）

| 等級 | 對手做到什麼 |
|---|---|
| **Total break（完全破解）** | 還原出金鑰 $k$ |
| **Universal break（普遍破解）** | 能對**每一則**訊息產生有效 tag |
| **Existential break（存在性破解）** | 能對**某一則**訊息產生一個**新的**有效 tag |

> **我們要求 MAC 能擋住 existential break！！**

**為什麼挑最弱的破解方式當標準**：擋住「最容易的破解」＝**最強的安全保證**。對手只要能偽造**任何一則**訊息（哪怕是一則毫無意義的亂碼）就算贏。

### EUF-CMA（p16）

**E**xistentially **U**n**f**orgeable against **C**hosen **M**essage **A**ttacks
（選擇訊息攻擊下的存在性不可偽造）

```
        𝒜                                      挑戰者
                                            k ← K
        ────────── m₁ ──────────▶
        ◀──── t₁ = MAC(k, m₁) ───
        ────────── m₂ ──────────▶
        ◀──── t₂ = MAC(k, m₂) ───
                  ⋮
        ───────── (m, t) ───────▶      若 (m,t) ≠ (mᵢ,tᵢ) 對所有 i
                                       且 Ver(k,m,t) = 1
                                       → 對手獲勝
```

$$\Pr\Big[(m,t) \leftarrow \mathcal{A}^{\mathrm{MAC}(k,\cdot)}(1^n) \;:\; \mathrm{Ver}(k,m,t) = 1 \;\wedge\; (m,t) \notin Q\Big] = \mathrm{negl}(n)$$

其中 $Q$ 是 $\mathcal{A}$ 問過的那些 $(m_i, t_i)$ 的集合。

> ⚠️ **一個值得注意的細節**：獲勝條件寫的是 **$(m,t) \notin Q$**，也就是**整個對**要是新的 —— 而不是「$m$ 要是新的」。
>
> 這表示：**對一則已經問過的訊息 $m_i$，產生一個「不同的」有效 tag，也算偽造成功。**
>
> 這通常叫 **strong EUF-CMA（強不可偽造）**。教科書上的標準 EUF-CMA 常常只要求 $m \notin \{m_i\}$（弱版）。若 MAC 是確定性的，兩者其實一樣（因為每則訊息只有一個有效 tag）；本堂的建構正好都是確定性的。

---

## 5. 等等⋯⋯加密不就解決了嗎？

（投影片 p17–19）**這一節是本堂最重要的觀念。**

### 直覺上的誤解

「我把訊息加密了，Eve 看不懂，那她怎麼竄改？」

### 反例 1：One-time pad

```
   Alice ──── m ⊕ k ────▶ 【Eve】 ──── m' ⊕ k ────▶ Bob
```

Eve 看不懂 $m$，但她**可以把密文 XOR 上 $(m \oplus m')$**：

$$(m \oplus k) \oplus (m \oplus m') = m' \oplus k$$

Bob 解出來就是 $m'$，**而且他完全不會發現**。

**Eve 不需要知道 $m$ 是什麼，就能把它改成 $m'$。**

### 反例 2：連我們的 PRF 加密方案也一樣

```
   Alice ── (r, f_k(r) ⊕ m) ──▶ 【Eve】 ── (r, f_k(r) ⊕ m') ──▶ Bob
```

一模一樣的招數。

### 結論

> **One-time pad（以及一般的加密方案）是 malleable（可鍛造 / 可延展的）。**
>
> **Privacy and Integrity are very different goals!**
> （隱私與完整性是完全不同的目標！）

**影片 L15 [45:20] 的說法更直白：**

> 「這一點非常重要，我們之後會一再回來講：**隱私和認證是完全不同的目標。** 你絕不該把其中一個誤認成另一個。**你不該把加密方案當成認證方案用。**」
>
> 他還反過來提醒：也有加密方案**本身就是**從 MAC 的失敗案例來的，而 MAC 也不提供隱私 —— 「這個建構隱藏了訊息，那個沒有」。**兩邊都不能互相代用。**

> 💡 **「malleable」這個詞記起來。** 它是說：你可以在**不知道明文**的情況下，把密文改成「解出來是某個相關明文」的樣子。之後 lec19 講 homomorphic encryption 時，這個性質會從 bug 變成 feature。

---

## 6. 用 PRF 造 MAC

（投影片 p20）

```
Gen(1ⁿ): 產生 PRF 金鑰 k ← K
MAC(k, m): 輸出 f_k(m)
Ver(k, m, t): 若 f_k(m) = t 則 Accept，否則 Reject
```

**就這樣。** MAC 就是 PRF 本身。

**安全性**：第 1 節那條**不可預測性引理**基本上已經證完了 —— 對手問了多項式多個 $m_i$ 拿到 $f_k(m_i)$，要偽造就得對一個新的 $m$ 產生 $f_k(m)$，那正是引理說做不到的事。

---

## 7. Replay Attack（重播攻擊）

（投影片 p21）

### 問題

> 對手可以把一組**舊的、有效的** $(m, \text{tag})$ **在稍後重新送一次**。
>
> **而且我們的安全定義並沒有排除這件事。**

為什麼定義擋不住：那組 $(m, t)$ 是**真的有效**的，$\mathrm{Ver}$ 當然會接受。EUF-CMA 只保證「偽造不出新的」，沒說「舊的不能重播」。

### 實務上的解法

- **加時間戳記**：例如送 $\big(m, T, \mathrm{MAC}(k, (m, T))\big)$，其中 $T = $ 2022 年 9 月 21 日 13:47。
- **加序號**：附在訊息上（**這會讓 MAC 演算法變成 stateful 的**）。

### 影片裡那個例子（L15 [44:06]–[45:20]）

Vinod 舉了一個很好記的例子：

> 「Eve 不該能把『**我給你十個 bitcoin**』這則訊息**一送再送** —— 那你就要給她十個、十個、又十個。」
>
> 「所以你不該只 MAC 訊息，而要 **MAC 訊息＋序號＋日期**。」

他也提醒了另一個 MAC **解決不了**的問題：

> 「MAC 擋得住**注入**訊息、擋得住**竄改**訊息，但擋不住**刪除**。Eve 隨時可以把訊息整個丟掉。」
>
> 序號可以幫上一點忙：Bob 如果收到第 $i$ 號之後直接收到第 $i+2$ 號，他**知道出事了**，可以要求重傳。但這屬於**協定層**要處理的事，不是 MAC 本身的責任。

> 💡 **記住 MAC 擋不住的兩件事：deletion（刪除）和 replay（重播）。**

---

## 8. 同時要隱私和完整性

（投影片 p22）

```
   Alice ──── ( c = (x, f_k(x) ⊕ m),  tag = f_{k'}(c) ) ────▶ Bob
  Keys k, k'                                                Keys k, k'
```

**先加密，再對密文做 MAC。用兩把不同的金鑰。**

> **MAC 給我們完整性，但不見得給隱私（why?）**

> 📎 **為什麼 MAC 不保護隱私**：本堂的 MAC 是 $f_k(m)$ —— **確定性的**。同一則訊息送兩次，tag 一模一樣，對手立刻知道「這兩則訊息相同」。這違反 IND-CPA（lec04）。影片 L15 [46:34] 也提到了這點。
>
> 更根本地說：MAC 的定義**從來沒要求**它隱藏任何東西。$\mathrm{MAC}(k,m) = m$ 本身（如果它安全的話）也會是一個合法的 MAC。

> **解法：Encrypt, then MAC（先加密，再 MAC）。**（更多內容在 Problem Set 2）

**注意兩個細節**：

1. **順序是 Encrypt-then-MAC** —— 對**密文**做 MAC，不是對明文。
2. **兩把金鑰 $k$ 和 $k'$ 必須不同。** 加密金鑰和 MAC 金鑰混用會出事。

第 10 節會看到這個組合的正式威力。

---

## 9. 長訊息的 MAC

（投影片 p23–27）

設 PRF 是 $f_k : \{0,1\}^B \to \{0,1\}^m$，但訊息 $M$ 很長（例如一份文件），要切成好幾塊 $M_1, M_2, \dots, M_t$。

投影片連續試了三個方法，**三個都被打破** —— 這一串失敗很值得看，因為每一次失敗都指出一個真正的攻擊面。

### Take 1：全部 XOR 起來再 MAC

$$\mathrm{MAC}(k, M_1, \dots, M_t) = f_k\Big(\bigoplus_i M_i\Big)$$

**Issue：任何 XOR 值相同的訊息，MAC 都一樣。**

例如把 $M_1$ 和 $M_2$ **交換**，XOR 不變 —— tag 也不變。甚至可以拼出完全不同的內容，只要 XOR 對得上。

### Take 2：每塊各自 MAC，再 XOR

$$\mathrm{MAC}(k, M_1, \dots, M_t) = \bigoplus_i f_k(M_i)$$

**Issue：可以把區塊重新排列。**

XOR 是可交換的，所以 $(M_1, M_2, M_3)$ 和 $(M_3, M_1, M_2)$ 的 tag 一樣。

### Take 3：把位置編號也放進去

把每塊縮成 $B/2$ bits，另外 $B/2$ bits 放**位置編號**：

$$\mathrm{MAC}(k, M_1, \dots, M_t) = \bigoplus_i f_k\big(\langle i \rangle \,\|\, M_i\big)$$

其中 $\langle i \rangle$ 是 $i$ 的 $B/2$-bit 表示。

**排列問題解決了** —— 現在第 3 塊如果換到第 1 個位置，編號不同，$f_k$ 的輸入就不同。

**Issue：Cut-and-paste attack（剪貼攻擊）。**

### 剪貼攻擊怎麼做（p26）

假設對手用 MAC oracle 問了三則三塊的訊息（大寫是「想偽造的內容」，小寫是「隨便什麼內容」）：

| 訊息 | tag |
|---|---|
| $(A, b, c)$ | $T_1 = f_k(1\|A) \oplus f_k(2\|b) \oplus f_k(3\|c)$ |
| $(a, B, c)$ | $T_2 = f_k(1\|a) \oplus f_k(2\|B) \oplus f_k(3\|c)$ |
| $(a, b, C)$ | $T_3 = f_k(1\|a) \oplus f_k(2\|b) \oplus f_k(3\|C)$ |

**把三個 tag XOR 起來**：

$$
\begin{aligned}
T_1 \oplus T_2 \oplus T_3 \;=\;& f_k(1\|A) \oplus f_k(2\|B) \oplus f_k(3\|C) \\
&\oplus \underbrace{\big[f_k(1\|a) \oplus f_k(1\|a)\big]}_{= 0} \oplus \underbrace{\big[f_k(2\|b) \oplus f_k(2\|b)\big]}_{= 0} \oplus \underbrace{\big[f_k(3\|c) \oplus f_k(3\|c)\big]}_{= 0} \\[4pt]
=\;& f_k(1\|A) \oplus f_k(2\|B) \oplus f_k(3\|C) \\[4pt]
=\;& \mathrm{MAC}_k(A \| B \| C)
\end{aligned}
$$

**小寫的部分成對出現，全部消掉了。** 對手從沒問過 $(A,B,C)$，卻算出了它的有效 tag。**EUF-CMA 被打破。**

> 💡 **失敗的根源**：XOR 結構讓對手可以「線性組合」已知的 tag。他從三個方程式解出了第四個。

### 正確做法：隨機化（p27）

**Bellare–Guerin–Rogaway 的隨機化建構**：

$$\mathrm{MAC}_k(M_1, \dots, M_t; r) = \Big(\, r, \;\; f_k(r) \oplus \big(\bigoplus_i f_k(\langle i \rangle \| M_i)\big) \,\Big)$$

每次 MAC 時挑一個**新的隨機 $r$**，用 $f_k(r)$ 當作「遮罩」蓋住那個 XOR 結果。

**為什麼這擋住剪貼攻擊**：每一則訊息的 tag 都被一個**不同的、不可預測的**值遮住了。對手再把 tag XOR 起來，遮罩不會成對消掉 —— 它們是 $f_k(r_1), f_k(r_2), f_k(r_3)$，三個不同的隨機值。

> **Proof: Exercise ☺**（投影片說，跟秘密金鑰加密的證明類似。）

---

## 10. Hash-then-Sign

（投影片 p28）

另一條路：**先壓縮，再 MAC**。

設 $H : \{0,1\}^* \to \{0,1\}^B$ 是一個 **collision resistant hash function (CRHF，碰撞阻抗雜湊函數)**：

- **公開**的函數，把任意長的訊息壓縮成 $B$ bits。
- **難以找到** $x, x'$ 使得 $H(x) = H(x')$。

那麼：

$$\mathrm{MAC}_k(m) = f_k\big(H(m)\big)$$

**Exercise：證明這是 EUF-CMA secure 的 MAC！**

> 📎 **證明的骨架**：若對手偽造出 $(m, t)$ 且 $m$ 沒問過，則要嘛
> (a) $H(m) = H(m_i)$ 對某個問過的 $m_i$ —— 那對手**找到了碰撞**，打破 CRHF；要嘛
> (b) $H(m)$ 是全新的值 —— 那對手在一個新的輸入上預測出了 $f_k$，打破 PRF。
> 兩種都不可能，故安全。

> 💡 注意 $H$ 是**公開**的（不需要金鑰），金鑰只用在 $f_k$ 上。CRHF 本身是 lec12–13 的主題。

---

## 11. IND-CCA2：對手能操弄密文時

（投影片 p29–33）

### 先回憶 IND-CPA（p30）

**Indistinguishable against chosen-plaintext attack**：對手有 **$\mathrm{Enc}$ oracle**。

```
        𝒜                                        挑戰者
                                              k ← K
  poly(n) 次 { ──── m ────▶
             { ◀── Enc(k,m) ──
             ───── m₀*, m₁* ────▶            b ← {0,1}
             ◀──── Enc(k, m_b) ───
  poly(n) 次 { ──── m ────▶
             { ◀── Enc(k,m) ──
             ───────  b′  ────────▶          b′ = b 則獲勝
```

注意 oracle 在**挑戰前後都能用**。

> **Exercise：這與 lec04 的定義等價。**

### IND-CCA2（p31）

**Indistinguishable against chosen-ciphertext attack**：對手有 **$\mathrm{Enc}$ 和 $\mathrm{Dec}$ 兩個 oracle**。

```
        𝒜                                           挑戰者
                                                 k ← K
  poly(n) 次 { ──── m, c ────▶
             { ◀── Enc(k,m), Dec(k,c) ──
             ───── m₀*, m₁* ────▶               b ← {0,1}
             ◀──── c* = Enc(k, m_b) ───
  poly(n) 次 { ──── m, c ────▶                   ⚠️ 檢查 c ≠ c*
             { ◀── Enc(k,m), Dec(k,c) ──
             ───────  b′  ────────▶             b′ = b 則獲勝
```

**唯一的限制：挑戰之後，對手不能把 $c^*$ 本身丟進 $\mathrm{Dec}$ oracle。**（否則太瞎了，直接解開就知道答案。）

> **除此之外，別的密文都可以解。** 這是一個非常強的模型 —— 但它對應真實情境：伺服器常常會對收到的密文做解密、然後把結果（或至少「解密成不成功」）洩漏出去。

### 我們的方案不是 IND-CCA2 安全的（p32）

回憶 lec04 的方案：$\mathrm{Enc}(k, m; r) = \big(r,\; f_k(r) \oplus m\big)$。

**攻擊**（利用第 5 節那個 malleability）：

1. 對手送出 $m_0^*, m_1^*$，拿到挑戰密文
   $$c^* = \big(r,\; f_k(r) \oplus m_b^*\big)$$
2. 挑一個 $s \ne 0$，構造
   $$c = \big(r,\; f_k(r) \oplus m_b^* \oplus s\big)$$
   **注意 $c \ne c^*$**（因為 $s \ne 0$），所以**這是合法的 oracle 查詢**。
3. 把 $c$ 丟進 $\mathrm{Dec}$ oracle，拿回
   $$m_b^* \oplus s$$
4. XOR 掉 $s$，**還原出 $m_b^*$**，直接看出 $b$ 是 0 還是 1。

**對手以機率 1 獲勝。**

投影片的結語很傳神：

> **If only it were hard to create a valid ciphertext to decrypt….**
> （要是「造出一個有效的、值得拿去解密的密文」是困難的，那該有多好⋯⋯）

**這句話就是解法的提示。**

### 修法：Encrypt-then-MAC（p33）

設 $(\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ 是 IND-CPA 安全的。造新的三元組：

- **$\mathrm{Gen}(1^n)$**：產生加密金鑰 $k \leftarrow K_{\text{SKE}}$ **和** MAC 金鑰 $k' \leftarrow K_{\text{MAC}}$。
- **$\mathrm{Enc}'(k, k', m)$**：輸出
  $$c = \mathrm{Enc}(k, m), \qquad t = \mathrm{MAC}(k', c)$$
  密文是 $(c, t)$。
- **$\mathrm{Dec}'(k, k', (c,t))$**：若 $\mathrm{Ver}(k', c, t) = \text{Reject}$，輸出 $\bot$；否則輸出 $\mathrm{Dec}(k, c)$。

> **Intuition：Dec oracle 變得毫無用處，因為對手很難產生出有效的 tag $t$。**

**為什麼這正好回答了上面那句話**：對手想操弄密文（把 $c^*$ 改成 $c$），但他改完之後**沒辦法補上對應的有效 tag** —— 那需要 MAC 金鑰 $k'$。所以 $\mathrm{Dec}'$ 會直接回 $\bot$，什麼資訊都不給。

> 💡 **整堂課在這裡收束了**：
> - 加密給你**隱私**，但它是 malleable 的。
> - MAC 給你**完整性**，但不給隱私。
> - **把兩個正確地黏起來（Encrypt-then-MAC，兩把金鑰）**，就得到能擋住主動對手的 IND-CCA2 安全。

---

## 名詞對照表

| 英文 | 中文 | 說明 |
|---|---|---|
| friend-or-foe identification | 敵我識別 | 證明「我是我」 |
| person/man-in-the-middle | 中間人 | 能竊聽也能竄改的對手 |
| impersonate | 冒充 | |
| challenge-response | 挑戰－回應 | 丟隨機 $r$，回 $f_s(r)$ |
| unpredictability | 不可預測性 | 問過多項式多點後仍猜不中新的點 |
| $\omega(\log n)$ | 超對數 | 比任何 $c\log n$ 都成長得快 |
| hypothesis class | 假設類 | 學習理論的概念 |
| message authentication code (MAC) | 訊息認證碼 | |
| tag | 標籤 | MAC 的輸出 |
| chosen message attack (CMA) | 選擇訊息攻擊 | 對手有 MAC oracle |
| total / universal / existential break | 完全 / 普遍 / 存在性破解 | 三種強度 |
| EUF-CMA | 選擇訊息攻擊下存在性不可偽造 | MAC 的標準安全定義 |
| forge | 偽造 | |
| malleable | 可鍛造的 | 不知明文也能把密文改成相關明文 |
| replay attack | 重播攻擊 | 重送舊的有效訊息 |
| deletion | 刪除 | MAC 擋不住的另一件事 |
| integrity | 完整性 | 訊息沒被改過 |
| privacy | 隱私 | 訊息看不懂 |
| Encrypt-then-MAC | 先加密再 MAC | 正確的組合順序 |
| cut-and-paste attack | 剪貼攻擊 | 把多個 tag 線性組合出新的 |
| collision resistant hash function (CRHF) | 碰撞阻抗雜湊函數 | 難找 $H(x) = H(x')$ |
| hash-then-sign | 先雜湊再簽 | $f_k(H(m))$ |
| IND-CCA2 | 適應性選擇密文攻擊下不可區分 | 對手有 Enc 和 Dec oracle |
| decryption oracle | 解密預言機 | |

---

## 📎 外部補充（非課堂內容）

> 以下不在投影片、也不在 L15 影片裡，是我額外加的。

**1. CCA1 vs CCA2 的差別**
投影片只講 **CCA2**。名字裡的 **2** 指的是「**adaptive（適應性）**」—— 對手在**拿到挑戰密文之後**仍然能用 $\mathrm{Dec}$ oracle。相對地 **CCA1**（有時叫 “lunchtime attack”，午餐時間攻擊）只允許在挑戰**之前**使用 oracle。CCA2 嚴格更強，也是現代的標準要求。

**2. 為什麼一定要 Encrypt-then-MAC，而不是別的順序**
另外兩種常見組合都有問題：
- **MAC-then-Encrypt**（先對明文 MAC，再把 $(m,t)$ 一起加密）：一般情況下**不保證** CCA2 安全。歷史上 TLS 用過這個順序，衍生出 Lucky 13 等攻擊。
- **Encrypt-and-MAC**（分別對明文加密、對明文 MAC，兩個都送）：直接洩漏隱私，因為確定性的 MAC 會暴露訊息相等性。

**Encrypt-then-MAC 是唯一一個「只要底層元件安全就一定安全」的組合。** 這個結果來自 Bellare–Namprempre (2000)。

**3. 為什麼兩把金鑰不能共用**
用同一把 $k$ 同時做加密和 MAC，安全證明會垮掉 —— 兩個安全定義各自假設「金鑰只給自己用」。實務上會用 **key derivation** 從一把主金鑰導出兩把子金鑰。

**4. 現代做法：AEAD**
實務上現在很少手動組裝 Encrypt-then-MAC，而是用 **AEAD（Authenticated Encryption with Associated Data）**，例如 **AES-GCM** 或 **ChaCha20-Poly1305** —— 一個原語同時給隱私和完整性，避免組裝錯誤。概念上它就是這堂課的結論被打包起來。

**5. 延伸閱讀**
- Katz–Lindell，第 4 章（MAC、CBC-MAC、CCA 安全、認證加密）
- Boneh–Shoup（在 `books/`），第 6 章（MAC）、第 9 章（認證加密）
- Kearns & Valiant, *Cryptographic Limitations on Learning Boolean Formulae and Finite Automata*, JACM 1994

---

## ⚠️ 存疑處

| 位置 | 問題 |
|---|---|
| **影片覆蓋** | 本堂有三段**完全沒有影片**：challenge-response（p3–6）、學習理論（p8–9）、IND-CCA2（p30–33）。我檢查過 L15 和 L16 都沒有。這些段落的內容**全部來自投影片**，我的直覺補充都標在 📎 裡。 |
| 投影片 p9 | 只有一張標題頁「Machine Learning and Cryptography (A quick aside)」，**沒有任何內容**。實際講了什麼無從得知。 |
| 投影片 p4, p23–27 | 數學上下標在 PDF 文字層裡壞掉（`{0,1}ℓ → {0,1}#`、`𝑓J : 0,1 K → 0,1 L`、`𝑀M , 𝑀N , … , 𝑀O`）。我按上下文還原成 $f_k : \{0,1\}^\ell \to \{0,1\}^m$ 與 $f_k : \{0,1\}^B \to \{0,1\}^m$，**請對照原 PDF 的圖確認**。 |
| 投影片 p16 | 獲勝條件是 $(m,t) \notin Q$（整個對要新），這是 **strong** EUF-CMA。多數教科書的標準 EUF-CMA 只要求 $m$ 是新的。本堂的 MAC 都是確定性的，兩者等價，但換到機率性 MAC 時會有差別。 |
| 投影片 p22 | 「MACs give us integrity, but not necessarily privacy **(why?)**」—— 投影片提問但沒答。我的答案標在 📎 裡。 |
| 投影片 p27, p28 | BGR 隨機化建構的安全性證明、以及 hash-then-sign 的證明，**都留作練習**，投影片沒有寫。p28 的證明骨架是我補的。 |
| 投影片 p30 | 「Exercise: This is equivalent to definition from Lec 4」—— 兩個定義的等價性留作練習。lec04 的版本是反覆送訊息對；這裡是先用 oracle、再送一對挑戰。 |
| L15 字幕品質 | 舊版 ASR，無標點，術語錯誤極多（MAC 被寫成 “Mac”、“max”、“Max”，challenger 被聽成別的字）。我只引用了能與投影片互相印證的部分。 |
| L15 涵蓋範圍 | L15 大約 [52:52] 之後轉向數位簽章與 CRHF，那是 Fall 2022 的 **lec11–13**。依 BRIEF 的規則沒有寫進本筆記。 |
