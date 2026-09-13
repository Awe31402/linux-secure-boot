# Lecture 1 — Introduction, Perfect Secrecy, One-Time Pad

> **來源說明**
> - 投影片：`slides/lec01.pdf`（MIT 6.5620/6.875/18.425, **Fall 2022**, Vinod Vaikuntanathan）
> - 影片：<https://youtu.be/jDsfV2ohFPs> — “6.875 (Cryptography) L1: Introduction, One-Time Pad”，**2018 年**的錄影（上傳者 Andrew Xia），1:20:44。
>
> MIT 沒有公開 Fall 2022 的錄影，這是唯一一套線上影片。**lec01 兩邊講的是同一套內容**，所以可以互補。但注意：影片編號從 L2 起就對不上 Fall 2022 的投影片（播放清單 L2 = One-Way Functions，Fall 2022 lec02 = PRG）。
>
> 字幕是 YouTube 自動生成，品質差（一路把 cryptography 聽成 "photography"）。正式內容一律以投影片為準；下面標 `⚠️` 的地方是我判斷字幕不可靠處。標 `📎 補充` 的區塊不是課堂內容，是我額外加的。

---

## 一句話總結

**完美的加密是做得到的**（one-time pad），**但代價是金鑰必須至少和訊息一樣長** —— 而這個代價是所有完美方案都逃不掉的，所以整門課接下來要做的事，就是把「對手無限強」這個假設放寬掉。

---

## 這堂課要回答三個問題

1. 「這個加密是安全的」到底**是什麼意思**？（要一個數學定義，不是一句話）
2. 這種安全**做得到嗎**？
3. 做得到的話，**要付什麼代價**？

答案分別是：Shannon 的 perfect secrecy、one-time pad、以及 $|\mathcal{K}| \ge |\mathcal{M}|$。

---

## 1. 這門課在幹嘛

### Crypto ≠ Cryptocurrency

6.875 **不是**在講區塊鏈或加密貨幣，也不是「可信賴的機器學習」。它講的是這些東西底下那層地基：digital signatures、zero-knowledge proofs、public-key encryption、homomorphic encryption、threshold cryptography、pseudorandomness。

### 思想源頭

兩個人，幾乎同時，都因為二戰而碰上密碼學：

| 人 | 密碼學工作 | 順帶開創的領域 |
|---|---|---|
| Claude Shannon | *Communication Theory of Secrecy Systems*（1945，機密，約十年後才公開） | *A Mathematical Theory of Communication*（1948）→ information theory |
| Alan Turing | Enigma 的破譯（約 1938–39） | *On Computable Numbers*（1936）→ computer science |

有趣的地方在於：**兩個人的密碼學論文都寫在他們的成名理論之前。** Shannon 那篇機密的密碼學論文比 1948 那篇資訊理論奠基作還早。這堂課的主題正是 Shannon 那篇在做的事：**替「安全」下定義**。

古典密碼學基本上是戰時產物（軍事應用）。現代密碼學則是隨網際網路長出來的 —— 陌生人之間要能安全通訊、要能做電子商務。之後又擴張到不只是保密，還要**驗證**（訊息真的是我發的、沒被改過），再到**運算本身的隱私**（把程式交給別人跑，同時保住正確性與隱私）。

### 三大主題

**主題 1：無所不在、最壞情況的對手（The Omnipresent, Worst-case Adversary）**

- 核心作法：**把對手模型化** —— 她知道什麼、她能做什麼、她的目標是什麼。
- **定義是我們的朋友。定義不出來的東西，就實現不了。**
- 這門課最大的收穫其實是一種思考方式：cryptographic / adversarial thinking。

**主題 2：計算困難性是我們的工具（從 lecture 2 開始）**

- 核心概念是 **the cryptographic leash（密碼學的狗鍊）**：用計算困難性來「馴服」對手。
- 困難問題的古典來源是**數論**。近年則加上幾何、編碼理論、組合數學。
- 一句總結：**密碼學是「有用的困難」的科學**（the science of useful hardness）。

> 投影片引了 G. H. Hardy 的話，說數論「遠離人類日常活動、因而保持溫和潔淨」—— 這在今天讀起來相當諷刺，數論正是現代加密的引擎。

**主題 3：用歸約（reduction）證明安全**

安全證明長這樣：

> 「如果存在一個（有效率的）對手能打破方案 A 對定義 D 的安全性，那就存在一個（有效率的）演算法能分解大數。」

具體一點，課堂上是這樣描述的（[13:28]）：假設對手能在時間 $t$、以機率 $\varepsilon$ 打破系統，我們就把它當**子程序**用，造出一個演算法，在時間 $\mathrm{poly}(t)$、以機率 $\mathrm{poly}(\varepsilon)$ 解掉某個公認的數學難題。既然那個難題被認為解不了，這樣的對手就不能存在。

兩個要注意的地方：

- 這是**假設性**的。我們不知道 factoring 真的難 —— 那是未解問題。我們是把安全性**歸約**到這些假設上。
- 這比 6.045 的 NP-hardness 歸約難得多：我們的歸約是**機率性**的，而且要處理「對手只有部分機率成功」這件事。
- 心態上要轉一下：你在這門課裡會**一直在設計演算法**（解難題的演算法），只是設計它的目的是拿來**證明安全性**。

**「Science wins either way」**（投影片引用 Silvio Micali）：我們設計一個系統，結果只有兩種 —— 要嘛它非常安全，要嘛有人打破它，而那代表某個大家以為很難的數學問題其實不難。兩種都是科學的勝利。

課堂上舉的例子（[15:35]）：Peter Shor 當年在研究整數分解，正是因為 factoring 在密碼學上太重要；他最後給出的是量子演算法。

---

## 2. 問題設定：Secure Communication

### 場景

Alice 想傳訊息 $m$ 給 Bob，而不讓竊聽者 Eve 知道。

**SETUP（關鍵前提）：Alice 和 Bob 事先見過面，約好了一把秘密金鑰 $k$。**

這個前提很強 —— 現實中 Amazon 和你並沒有事先碰面過。整堂課後面（public-key encryption）就是要拆掉它。但這堂先接受它。

### Secret-key Encryption（又稱 symmetric-key encryption）

一個加密方案是**三個（可能是機率性的）多項式時間演算法** $(\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$：

- **$\mathrm{Gen}$（金鑰生成）**：$k \leftarrow \mathrm{Gen}(1^\lambda)$
- **$\mathrm{Enc}$（加密）**：$c \leftarrow \mathrm{Enc}(k, m)$
- **$\mathrm{Dec}$（解密）**：$m \leftarrow \mathrm{Dec}(k, c)$

三個空間：訊息空間 $\mathcal{M}$、金鑰空間 $\mathcal{K}$、密文空間 $\mathcal{C}$。

### 兩個要求

**Correctness（正確性）**：$\mathrm{Dec}(k, \mathrm{Enc}(k, m)) = m$。Alice 加密什麼，Bob 就解出什麼。

**Security（安全性）**：這整堂課要定義的東西。

### 為什麼每個演算法可能需要隨機性

這一段投影片只寫了一行「Gen has to be probabilistic」，影片講得比較細（[34:47]–[37:28]）：

- **$\mathrm{Gen}$ 必須是機率性的。** 對手的一種攻擊就是「把所有可能的金鑰試一遍」（exhaustive search）。如果 $\mathrm{Gen}$ 是確定性的，它只會吐出一把固定的金鑰，對手直接照著跑一次就拿到了。所以金鑰空間必須夠大、而且金鑰要隨機選。
- **$\mathrm{Enc}$ 也需要是機率性的。** 確定性加密表示同一個訊息永遠對到同一個密文。課堂上預告：**課程很早就會證明，除非加密是機率性的（同一個訊息可以對到很多個密文），否則沒辦法達到我們想要的安全性。**
- **$\mathrm{Dec}$ 通常不需要隨機性**（答案是唯一的），但也不是不能有。而且如果願意把 correctness 放寬成「以 $1 - \text{negligible}$ 的機率解對」，反而能換到一些額外性質 —— 課堂上提到 **deniability（可否認性）**：正因為存在極小的出錯機率，你可以對第三方否認自己送過某個訊息。

> 💡 這是一個之後會反覆出現的模式：**把定義放寬一點點，常常能換到全新的能力。**

### 對手模型：The Worst-case Adversary

Eve 是：

- 一個**計算能力無上限（computationally unbounded）**的任意演算法 —— 指數時間、指數空間都隨她用。這種對手現實中不存在，但如果我們能擋住她，那就真的高枕無憂。
- **她知道 $\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec}$ 這三個演算法**，但不知道金鑰，也不知道 Alice/Bob 內部的隨機硬幣。
  這就是 **Kerckhoff's principle**（又稱 Shannon's maxim）。
- 她**看得到**通道上的密文，但（這一講）**不能修改**它們。

**為什麼要假設 Eve 知道演算法？** 課堂上講得很清楚（[42:48]）：重點不是我們真的會把程式碼寄給對手。重點是這是一門理論課 —— **我們不能假設她不知道**。現實中對手極可能知道你用的是 RSA 還是什麼。**讓對手知道越多、我們還能證明安全，這個結論就越有價值。**

於是問題變成一句話：

> **Security Definition: What is she trying to learn?（她到底想學到什麼？）**

### 我們想要多強的安全？

課堂上是一路加碼上去的（[43:47]–[46:05]）：

1. Eve 不該能**還原出整個訊息** $m$。—— 這當然要，但遠遠不夠。
2. Eve 不該能學到**第一個 bit**、或**任何一個 bit**、或所有 bit 的 XOR。
3. Eve 不該能學到**訊息的任何部分資訊（partial information）**。
4. 而且不只是「不能有把握地學到」，是**連以小機率猜對都不行**。
5. 而且要對**所有訊息**成立，不能只保護某些訊息。
6. 送**多個**訊息時，Eve 也不該能學到訊息之間的**關係** —— 例如「這兩個訊息是不是一樣」、「前綴是不是一樣」。

第 6 點有個歷史例子：Enigma 的一個弱點就是德軍每則訊息開頭都是同一句問候語。

---

## 3. 定義一：Shannon's Perfect Secrecy

### 想法

$$\textbf{A-posteriori} = \textbf{A-priori}$$

看到密文**之前**你對訊息的猜測，跟看到密文**之後**你對訊息的猜測，**完全一樣**。也就是：那條線上的東西你不看也罷。

### 形式定義

> ⚠️ 投影片 p.18 這格公式框是空的（Vinod 當場寫在黑板上）。下面的公式取自投影片 p.21 “WE WANT (SEC)” 那一行，與影片 [46:05]–[49:39] 的口述一致。

$(\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ 滿足 **perfect secrecy**，若：

$$\forall \mathcal{M},\; \forall m \in \mathrm{Supp}(\mathcal{M}),\; \forall c \in \mathrm{Supp}(\mathcal{C}):$$
$$\Pr[\mathcal{M} = m \mid \mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c] \;=\; \Pr[\mathcal{M} = m]$$

拆開來讀：

- $\mathcal{M}$ 是訊息空間上的**任意機率分布** —— 我們不假設訊息怎麼產生。Eve 甚至可以完全知道這個分布（例如「Alice 說英文」）。
- $\mathcal{K}$ 是金鑰的隨機變數（由 $\mathrm{Gen}$ 決定的分布）。
- 左邊是**後驗機率**（看到密文 $c$ 之後），右邊是**先驗機率**（看到之前）。
- 三個 $\forall$ 都很重要：對所有分布、所有訊息、所有密文都要成立。

**機率是對什麼取的？**（[50:45] 課堂問答，這題值得記）
同時對**訊息的選擇**和**金鑰的選擇**取。學生問了，Vinod 確認：是的，也包含金鑰。

### 一個常見誤解

有學生問：那 Eve 從密文學到關於**金鑰**的資訊呢？（[53:42]–[54:54]）

Vinod 的回答：這個定義**不需要**去管金鑰洩漏。因為我們要的是「訊息的資訊不外洩」。如果洩漏金鑰資訊會導致洩漏訊息資訊，那定義本身就已經擋住了。反之，洩漏了一些關於金鑰、卻對猜訊息毫無幫助的資訊，我們不在乎。

（不過課堂上也提到一個例外情境：如果金鑰洩漏會讓你發現「同一個訊息被送了兩次」，那就確實是訊息資訊了 —— 那正是下面 two-time pad 的問題。）

這個定義**極強**。用 Vinod 的話說（[56:22]）：機率完全不變，你**根本沒必要去看那條線**。很難想像還有更強的東西。

---

## 4. 定義二：Perfect Indistinguishability

### 為什麼要第二個定義

課堂上講了密碼學的一個標準做法（[56:22]）：**提出好幾個聽起來都合理的定義，然後證明它們等價。** 等價性給你信心 —— 你抓到的確實是「安全」這個概念本身，而不是某一種寫法的怪癖。

### 想法：一個圖靈測試

Eve 拿到一個密文，要猜自己在哪個世界：

| World 0 | World 1 |
|---|---|
| $k \leftarrow \mathcal{K}$ | $k \leftarrow \mathcal{K}$ |
| $c = \mathrm{Enc}(k, m)$ | $c' = \mathrm{Enc}(k, m')$ |

Eve 是一個 **distinguisher（區分器）**：拿到密文，猜自己在 World 0 還是 World 1。如果她辦不到，方案就是安全的。

### 形式定義

> ⚠️ 投影片 p.19 的公式框同樣是空的。下面取自投影片 p.21 “WE KNOW (IND)”，與影片 [58:02] 的口述一致。

$$\forall \mathcal{M},\; \forall m, m' \in \mathrm{Supp}(\mathcal{M}),\; \forall c \in \mathrm{Supp}(\mathcal{C}):$$
$$\Pr[\mathrm{Enc}(\mathcal{K}, m) = c] \;=\; \Pr[\mathrm{Enc}(\mathcal{K}, m') = c]$$

注意這裡的機率**只對金鑰取**（$m, m'$ 都固定住了）。意思是：$m$ 固定之後，還有選金鑰這個自由度，不同金鑰給出不同密文 —— 這就導出密文上的一個機率分布。定義要求：**$m$ 導出的密文分布，和 $m'$ 導出的密文分布，一模一樣。**

### 兩個定義的口味差在哪

- **Perfect secrecy** 說的是「關於訊息的**機率**完全沒變」。
- **Perfect indistinguishability** 說的是「**任兩個訊息**在密文上長得一樣可能」。第二個更貼近實戰直覺：Eve 想知道的往往就是二選一 —— 「attack」還是「don't attack」。

課堂上做了舉手投票（[61:29]），兩邊都有人選。答案是：**都對，它們等價。**

---

## 5. 定理：兩個定義等價

> **THEOREM.** 一個加密方案 $(\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ 滿足 perfect secrecy **若且唯若**它滿足 perfect indistinguishability。
>
> **PROOF.** Bayes 定理的簡單應用。

以下兩個方向都在投影片上完整寫出（p.21–23）。

### 方向 1：Indistinguishability ⟹ Secrecy

**已知（IND）**：$\forall \mathcal{M}, \forall m, m' \in \mathrm{Supp}(\mathcal{M}), \forall c \in \mathrm{Supp}(\mathcal{C})$，

$$\Pr[\mathrm{Enc}(\mathcal{K}, m) = c] = \Pr[\mathrm{Enc}(\mathcal{K}, m') = c] \;=:\; \alpha$$

（因為對所有 $m$ 都一樣，這個共同值可以命名為 $\alpha$ —— 它只跟 $c$ 有關，跟訊息無關。**這是整個證明的關鍵。**）

**要證（SEC）**：$\Pr[\mathcal{M} = m \mid \mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c] = \Pr[\mathcal{M} = m]$

**Key Observation：** $\forall m,\; \Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c] = \Pr[\mathrm{Enc}(\mathcal{K}, m) = c]$

證明（全機率公式）：

$$
\begin{aligned}
\Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c]
&= \sum_{m} \Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c \mid \mathcal{M} = m] \cdot \Pr[\mathcal{M} = m] \\
&= \sum_{m} \Pr[\mathrm{Enc}(\mathcal{K}, m) = c] \cdot \Pr[\mathcal{M} = m] \\
&= \alpha \sum_{m} \Pr[\mathcal{M} = m] \;=\; \alpha
\end{aligned}
$$

（最後一步用了 $\sum_m \Pr[\mathcal{M}=m] = 1$。）

**主證明（Bayes）：**

$$
\begin{aligned}
\Pr[\mathcal{M} = m \mid \mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c]
&= \frac{\Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c \mid \mathcal{M} = m] \cdot \Pr[\mathcal{M} = m]}{\Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c]} && \text{(Bayes)} \\
&= \frac{\Pr[\mathrm{Enc}(\mathcal{K}, m) = c] \cdot \Pr[\mathcal{M} = m]}{\Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c]} \\
&= \frac{\alpha \cdot \Pr[\mathcal{M} = m]}{\alpha} && \text{(key obs.)} \\
&= \Pr[\mathcal{M} = m]
\end{aligned}
$$

### 方向 2：Secrecy ⟹ Indistinguishability

**已知（SEC）**：$\Pr[\mathcal{M} = m \mid \mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c] = \Pr[\mathcal{M} = m]$

**要證（IND）**：$\Pr[\mathrm{Enc}(\mathcal{K}, m) = c] = \Pr[\mathrm{Enc}(\mathcal{K}, m') = c]$

$$
\begin{aligned}
\Pr[\mathrm{Enc}(\mathcal{K}, m) = c]
&= \Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c \mid \mathcal{M} = m] \\
&= \frac{\Pr[\mathcal{M} = m \mid \mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c] \cdot \Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c]}{\Pr[\mathcal{M} = m]} && \text{(Bayes)} \\
&= \Pr[\mathrm{Enc}(\mathcal{K}, \mathcal{M}) = c] && \text{(SEC：分子分母的 } \Pr[\mathcal{M}=m] \text{ 消掉)} \\
&= \Pr[\mathrm{Enc}(\mathcal{K}, m') = c] && \text{(對稱性：同樣的論證套在 } m' \text{ 上)}
\end{aligned}
$$

$\blacksquare$

### 為什麼這件事有價值

1. **信心**：兩個從不同角度出發的定義撞在同一點，代表我們抓對了概念。
2. **好用**：其中一個常常比另一個好操作。之後整門課會反覆出現 indistinguishability 型的定義（「這串數跟真隨機數分不出來」），因為它**特別好證**。

> 💡 這是密碼學的一個常態：一個概念有好幾個等價定義，但大家幾乎只用其中一個 —— 因為它最好用。

### 一個實用提醒（[64:03]）

這整堂課（甚至整門課）的機率工具其實少得驚人。主要就兩個：

- **union bound**：$\Pr[A \cup B] \le \Pr[A] + \Pr[B]$
- $\sum_m \Pr[\mathcal{M} = m] = 1$

Vinod 說這幾乎就是全部了。

---

## 6. 建構：One-Time Pad

好消息：**這麼強的定義，真的做得到。**

### 方案

設 $n$ 是訊息長度。金鑰、訊息、密文全都是 $n$-bit 字串。

- **$\mathrm{Gen}$**：隨機選一個 $n$-bit 字串，$k \leftarrow \{0,1\}^n$（就是丟 $n$ 次硬幣）
- **$\mathrm{Enc}(k, m)$**：輸出 $c = m \oplus k$
- **$\mathrm{Dec}(k, c)$**：輸出 $m = c \oplus k$

其中 $\oplus$ 是 bitwise XOR：

$$0 \oplus 0 = 1 \oplus 1 = 0, \qquad 0 \oplus 1 = 1 \oplus 0 = 1, \qquad a \oplus b = a + b \bmod 2$$

注意 $\mathrm{Enc}$ 和 $\mathrm{Dec}$ **都是確定性的** —— 隨機性全部集中在 $\mathrm{Gen}$。

### 正確性

$$c \oplus k = (m \oplus k) \oplus k = m \oplus (k \oplus k) = m \oplus 0 = m \quad \checkmark$$

### 安全性

> **Claim.** One-time pad 滿足 perfect indistinguishability（因此也滿足 perfect secrecy）。

**Proof.** 對任意 $m, m', c \in \{0,1\}^n$：

$$
\begin{aligned}
\Pr[\mathrm{Enc}(\mathcal{K}, m) = c]
&= \Pr[m \oplus \mathcal{K} = c] \\
&= \Pr[\mathcal{K} = c \oplus m] \\
&= \frac{1}{2^n} \\
&= \Pr[\mathcal{K} = c \oplus m'] \\
&= \Pr[m' \oplus \mathcal{K} = c] \\
&= \Pr[\mathrm{Enc}(\mathcal{K}, m') = c]
\end{aligned}
$$

$\blacksquare$

**直覺**：不管你要送哪個訊息，**恰好只有一把金鑰**會把它變成 $c$（就是 $k = c \oplus m$）。金鑰是均勻隨機的，所以每個訊息變成 $c$ 的機率都剛好是 $1/2^n$。密文完全不帶訊息的資訊。

---

## 7. 反例：One-Time Pad 不能重用

### 情境

Alice 用金鑰 $k$ 送了 $c_0 = m_0 \oplus k$。一週後，她**用同一把 $k$** 又送了 $c_1 = m_1 \oplus k$。

還是完美保密嗎？**不是。**

### 直覺（先看這個）

Eve 拿到 $c_0$ 和 $c_1$，可以算：

$$c_0 \oplus c_1 = (m_0 \oplus k) \oplus (m_1 \oplus k) = m_0 \oplus m_1$$

金鑰消失了。Eve 直接拿到兩個明文的 XOR。**特別是：如果 $m_0 = m_1$，她會看到 $c_0 \oplus c_1 = 0$ —— 立刻知道同一個訊息被送了兩次。**

### 形式反證（投影片 p.30–32）

把「送兩則訊息」看成一個 $2n$-bit 的方案（two-time pad）。Perfect indistinguishability 要求：對所有 $(m_0, m_1), (m_0', m_1'), (c_0, c_1) \in \{0,1\}^{2n}$，

$$\Pr[\mathrm{Enc}(k, m_0) = c_0 \wedge \mathrm{Enc}(k, m_1) = c_1] = \Pr[\mathrm{Enc}(k, m_0') = c_0 \wedge \mathrm{Enc}(k, m_1') = c_1]$$

我們只要找**一組**反例。取：

$$m_0 = m_1 = m, \qquad m_0' \ne m_1', \qquad c_0 = c_1 = c$$

左邊：兩個條件變成同一個條件，

$$\Pr[\mathrm{Enc}(k, m) = c] = \frac{1}{2^n}$$

右邊：要同時有 $m_0' \oplus k = c$ 和 $m_1' \oplus k = c$，也就是 $k = c \oplus m_0'$ 且 $k = c \oplus m_1'$。但 $m_0' \ne m_1'$，這兩個要求互相矛盾，**沒有任何金鑰能同時滿足**：

$$\Pr[\mathrm{Enc}(k, m_0') = c \wedge \mathrm{Enc}(k, m_1') = c] = 0$$

$1/2^n \ne 0$，定義被違反。$\blacksquare$

> 這也是為什麼它叫 **one-time** pad。

### 那換一個方案就好了？

課堂上緊接著問（[76:02]）：這個問題會不會只是 one-time pad 自己的毛病？也許有別的方案能安全地送多則訊息？

答案是：**沒有。** 這帶到下一節。

---

## 8. 壞消息：Shannon 的下界

> **THEOREM.** 對任何完美安全的加密方案，$|\mathcal{K}| \ge |\mathcal{M}|$。
>
> （金鑰空間至少要跟訊息空間一樣大 —— 也就是**金鑰至少要跟訊息一樣長**。）

### 用圖證（投影片 p.33–34）

反證。假設 $|\mathcal{K}| < |\mathcal{M}|$。

1. 任取一個密文 $c \in \mathcal{C}$。
2. 看看「所有可能解出 $c$ 的訊息」這個集合：$S = \{\, \mathrm{Dec}(k, c) : k \in \mathcal{K} \,\}$。
3. 每把金鑰最多貢獻一個訊息，所以 $|S| \le |\mathcal{K}| < |\mathcal{M}|$。
4. 因此**至少存在一個訊息 $\tilde{m} \in \mathcal{M}$ 不在 $S$ 裡** —— 沒有任何金鑰能把 $\tilde{m}$ 加密成 $c$。
5. 於是：
   $$\Pr[\mathrm{Enc}(\mathcal{K}, m) = c] > 0 \qquad \text{但} \qquad \Pr[\mathrm{Enc}(\mathcal{K}, \tilde{m}) = c] = 0$$
6. 這直接違反 perfect indistinguishability。$\blacksquare$

### 這代表什麼

Eve 看到 $c$，就算什麼都算不出來，她**至少知道 $\tilde{m}$ 不是那個訊息** —— 因為根本沒有金鑰能產生這個組合。這已經是資訊了。

實務上的殘酷後果（[78:28]）：

> 你想送 $n$ bits，就得先見面丟 $n$ 次硬幣。想送 $2n$ bits，要嘛再見一次面，要嘛第一次見面時就得**先知道**你這輩子總共要送多少 bits，然後一次丟夠。

這就是為什麼 one-time pad 雖然完美，卻幾乎沒法用。

---

## 9. 出路

問題出在哪？出在我們給 Eve 的能力太大了 —— **計算能力無上限**。

**放寬定義：**

> Eve 是一個任意的、**計算能力有限（computationally bounded）**的演算法。

加上數論 / 幾何 / 組合數學提供的困難問題，就進入了投影片說的 “the promised crypto land”：pseudorandomness、public-key encryption、zero-knowledge proofs、fully homomorphic encryption。

這是**下一講**的起點。

---

## 本講總結（投影片 p.36）

- **Secure communication** 是密碼學最典型的問題。
- 我們看到兩個**等價**的安全定義：Shannon 的 **perfect secrecy** 和 **perfect indistinguishability**。
- **One-time pad 達成了 perfect secrecy。**
- **嚴重限制**：任何完美安全的加密方案，金鑰都必須至少和訊息一樣長。
- **下一講**：用「計算能力有限的對手」來突破這個限制。

---

## 名詞對照表

| 英文 | 中文 | 說明 |
|---|---|---|
| plaintext / message $m$ | 明文 / 訊息 | 要保護的東西 |
| ciphertext $c$ | 密文 | 通道上跑的東西 |
| key $k$ | 金鑰 | Alice 和 Bob 共享的秘密 |
| message space $\mathcal{M}$ | 訊息空間 | 也用來指訊息上的機率分布 |
| key space $\mathcal{K}$ | 金鑰空間 | |
| ciphertext space $\mathcal{C}$ | 密文空間 | |
| secret-key / symmetric-key encryption | 對稱式加密 | 加解密用同一把金鑰 |
| eavesdropper | 竊聽者 | 只能看、不能改 |
| adversary | 對手 | 課堂上叫 Eve |
| computationally unbounded | 計算能力無上限 | 本講的對手模型 |
| Kerckhoff's principle | Kerckhoff 原則 | 對手知道演算法，只是不知道金鑰 |
| correctness | 正確性 | $\mathrm{Dec}(k,\mathrm{Enc}(k,m)) = m$ |
| perfect secrecy | 完美保密 | 後驗 = 先驗 |
| perfect indistinguishability | 完美不可區分性 | 任兩訊息的密文分布相同 |
| distinguisher | 區分器 | 猜自己在哪個世界的演算法 |
| a-priori / a-posteriori | 先驗 / 後驗 | 看到密文之前 / 之後 |
| support $\mathrm{Supp}(\cdot)$ | 支撐集 | 機率大於 0 的那些值 |
| one-time pad | 一次性密碼本 | $c = m \oplus k$ |
| XOR ($\oplus$) | 互斥或 | $a \oplus b = a + b \bmod 2$ |
| reduction | 歸約 | 用「打破方案的對手」造出「解難題的演算法」 |
| pseudorandomness | 偽隨機性 | 下一講開始 |
| deniability | 可否認性 | 放寬 correctness 換到的性質 |
| union bound | 聯集界 | $\Pr[A \cup B] \le \Pr[A] + \Pr[B]$ |

---

## 📎 外部補充（非課堂內容）

> 以下不在投影片、也不在影片裡，是我補上的背景。要跟課堂內容區分開來。

**1. 為什麼 $\mathrm{Gen}$ 的輸入寫成 $1^\lambda$**
投影片上 $\mathrm{Gen}(\ )$ 的括號是空的。慣例上會寫 $\mathrm{Gen}(1^\lambda)$，$\lambda$ 是 security parameter（安全參數），$1^\lambda$ 是 $\lambda$ 個 1 組成的字串（unary，一進位）。寫成 unary 是為了讓「多項式時間」以 $\lambda$ 為基準來衡量 —— 如果寫成二進位，輸入長度只有 $\log \lambda$，$\mathrm{poly}(\lambda)$ 時間就變成指數時間了。這只是技術性約定。

**2. Shannon 下界的資訊理論版本**
本講用的是計數論證。等價的資訊理論說法是 $H(K) \ge H(M)$（金鑰的熵至少要有訊息的熵那麼多）—— 這是 Shannon 原論文的形式。兩者結論相同。

**3. 「two-time pad」在現實中出過事**
重用 keystream 導致 $c_0 \oplus c_1 = m_0 \oplus m_1$ 的攻擊，歷史上真的發生過：冷戰時期的 VENONA 計畫就是靠蘇聯重複使用一次性密碼本才破譯的。WEP 的 IV 重用也屬於同一類問題。

**4. 延伸閱讀**
- Katz–Lindell, *Introduction to Modern Cryptography*, 第 2 章（perfect secrecy）
- Boneh–Shoup（在 `books/`），第 2 章
- Shannon, *Communication Theory of Secrecy Systems* (1949) —— 本講的原始論文

---

## ⚠️ 存疑處

| 位置 | 問題 |
|---|---|
| 投影片 p.18 | Perfect Secrecy 定義的公式框是**空白的**（課堂上寫黑板）。我用 p.21 “WE WANT (SEC)” 那一行補齊，並對照影片 [46:05]–[49:39] 確認一致。 |
| 投影片 p.19 | Perfect Indistinguishability 的公式框同樣空白。用 p.21 “WE KNOW (IND)” 補齊，對照影片 [58:02]。 |
| 投影片 p.26 | 有一張 OTP 證明的**中間狀態**投影片（式子只寫到一半），是動畫的中間格，不是漏字。 |
| 投影片 p.30 vs p.31 | p.30 的 Claim 寫 “**Two-time** Pad does not achieve...”，p.31 起改成 “**One-time** Pad does not achieve...”。指的是同一件事（重用 OTP），投影片用字不一致。 |
| 影片 [50:45] | 「機率是對誰取的」那段問答字幕破碎，但結論明確：**同時對訊息分布和金鑰取**。 |
| 影片行政段落 | 影片是 2018 年的，提到 Stellar、不同的 TA、「6 份 pset 最後一份可用 course project 取代」。**Fall 2022 的規則不同**（見投影片：6 份 pset 取最好的 5 份，95%；課堂參與 5%；Piazza + Gradescope）。以投影片為準。 |
| 整份字幕 | YouTube 自動字幕把 cryptography 一律聽成 "photography"，人名地名也大量錯誤。所有數學內容都已用投影片校正過。 |
