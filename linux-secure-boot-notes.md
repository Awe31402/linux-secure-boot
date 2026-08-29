# 讀書筆記：Secure Boot Encryption with Linux

> Rodolfo Giometti, *Secure Boot Encryption with Linux: Implementation for
> Embedded Developers*, Apress Pocket Guides, 2026。
> 涵蓋範圍：第 1 章、第 2 章、第 3 章的概念部分。
>
> **出處標示**：每節結尾先附一段 📄 **原文**（引自原書，未翻譯），
> 再標兩組頁碼——**書頁**（印在紙本上的頁碼）與 **PDF 頁**（PDF 檔的第幾頁）。
>
> ⚠️ 兩者的差值**不是固定的**。逐頁核對 PDF 上印出的頁碼後，
> 實際對應為：書頁 1–75 → +20、77–107 → +19、109–189 → +18、
> 191–215 → +17、217 以後 → +16
> （每章的開頭會少一頁，書頁 76、108、190、216 在這個 PDF 裡不存在）。
> 筆記裡所有 PDF 頁碼都是照這張表換算的。
>
> 原始檔：[linux-secure-boot.pdf](./linux-secure-boot.pdf)（252 頁）。
> 規格見 [linux-secure-boot-notes-brief.md](./linux-secure-boot-notes-brief.md)。

**這份筆記的目標**：讀完能不看書，把開機信任鏈從第一棒講到掛載 root filesystem。

---

## §0 讀這本書之前

> ⚠️ 本節不是書上的內容，是我自己加的定位說明。

**問題**：你上網搜「Linux secure boot」，找到的九成是**另一件事**。

有兩個世界，名字一樣、觀念相通，但零件完全不同：

| | PC 世界 | 這本書（嵌入式 ARM） |
|---|---|---|
| 誰是第一棒 | UEFI firmware | 晶片內的 ROM code |
| 信任的根 | 主機板裡的 UEFI 變數（PK/KEK/db） | 燒進晶片的 fuse |
| 誰簽的 | 微軟簽 shim，發行版簽自己的 | **你自己簽**，鑰匙你自己生 |
| 中間層 | shim → GRUB → kernel | SPL → TF-A / OP-TEE → U-Boot → kernel |
| 目標 | 擋 bootkit，讓 Linux 能在一般 PC 開機 | 擋複製、擋改機、關機時保護祕密 |
| 典型硬體 | x86 PC | i.MX8 / i.MX9 / STM32MP1 + Yocto |

**記住這句**：這本書裡沒有微軟、沒有 shim、沒有 UEFI db。整條信任鏈的鑰匙
都是你自己產、自己燒進晶片的。搜資料時關鍵字要用 `U-Boot`、`HAB`、`fitimage`、
`CAAM`，而不是 `shim`、`MOK`、`sbsign`。

**書的目標讀者**是資深嵌入式開發者，所以很多名詞它直接用不解釋。
這份筆記會把那些補上，統一收在 [§14 名詞小抄](#14-名詞小抄)。

---

# 第一部分：加密的基本零件（第 1 章）

這一整章在回答一個問題：**鑰匙要放哪裡，才不會被拿走？**

後面第 2、3 章講的每一件事，都建立在這章的答案上。所以雖然感覺離
「開機」很遠，還是得先看。

---

## §1 兩種鑰匙，別搞混

### 這在解決什麼問題

「安全」其實是兩件不同的事，需要兩種鑰匙：

- **簽章鑰匙（signature key）** → 回答「這是誰發的？有沒有被改過？」
- **加密鑰匙（encryption key）** → 回答「別人看不看得懂內容？」

搞混這兩個，後面整條信任鏈都會理解錯。

### 怎麼運作

- **簽章一定要用非對稱金鑰對**（私鑰簽、公鑰驗）。
  作法是先算檔案的雜湊（hash），再對雜湊簽名。
- **加密可以對稱也可以非對稱**，但因為速度，所以
  **本書從頭到尾只用對稱加密**。

書裡固定用這兩組演算法：

- 加密：**AES-256-CBC**
  - AES-256 = 打亂資料的主力
  - CBC 模式 = 每個區塊先跟前一個密文 XOR 再加密。
    為什麼要這樣？因為單純的區塊加密，「同樣的明文 → 同樣的密文」，
    看密文就能看出重複樣式。CBC 把這個弱點補掉。
- 簽章：**ECDSA + SHA-256**
  - ECDSA 基於橢圓曲線，比 RSA 金鑰更短、更有效率
  - SHA-256 產生固定 256 bit 的雜湊。改一個 bit，輸出整個變掉

### 小例子（OpenSSL）

```bash
# 加密
echo "Very secret message" | openssl enc -e -aes-256-cbc -K <key> -iv <iv> > secret.enc
# 雜湊
openssl dgst -sha256 /tmp/id.txt
# 產亂數
openssl rand 32 | od -tx1
```

### 名詞

- **非對稱 / 對稱**：非對稱有兩把（公鑰、私鑰）；對稱只有一把，加解密同一把
- **IV（initial vector）**：CBC 的起始亂數，讓同樣的明文每次產出不同密文

> 📄 **原文**　書 p.1 ｜ PDF p.21
>
> In cryptography, the use of signature keys or encryption keys is intended
> for two different purposes. The former are used to ensure authenticity and
> integrity; that is, the goal is to verify who sent the data and that the data has
> not been altered since it was signed. While the latter are used to ensure
> confidentiality, so the goal is to make data unreadable to anyone except the
> intended recipient. To do a digital signature, we must use an asymmetric key
> pair, while for encryption, we can use asymmetric or symmetric encryption.
> [...] However, due to speed issues, all CPUs use symmetric encryption for
> securing their code, so from now until the end of this book, we are going to use
> symmetric encryption only.

📖 **書頁 1–5** ｜ PDF 頁 21–25 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=21)

---

## §2 為什麼不能把鑰匙寫在指令裡

### 這在解決什麼問題

看回 §1 那三行指令，有個致命問題：

```bash
openssl enc -e -aes-256-cbc -K 0123456789abcdef...
                            ^^^^^^^^^^^^^^^^^^^^^^
                            鑰匙就這樣裸在命令列上
```

任何有 root 權限的行程都看得到。在嵌入式裝置上，這等於沒有保護——
攻擊者拿到 root 就拿到你所有的鑰匙。

**這一整本書，本質上就是在解這個問題**：怎麼讓「就算有 root 也讀不到鑰匙」。

### 怎麼運作：Linux Crypto API

答案的第一步：**把加解密的動作搬進 kernel**。使用者空間只說「幫我用第 N 號
鑰匙加密這段資料」，鑰匙本身從頭到尾不出 kernel。

- kernel 內建一整套加密演算法，可以用 `cat /proc/crypto` 看
- 同一個演算法（例如 `cbc(aes)`）可能有**多個實作**：純軟體的、
  CPU 指令加速的（`cbc-aes-ce`）、專用硬體做的（`cbc-aes-caam`）
- 每個實作有 **priority**。你要 `cbc(aes)`，kernel 挑 priority 最高的那個
  （同分就隨便挑一個）。想指定就直接寫 driver 名字（`cbc-aes-ce`）
- 使用者空間透過 **AF_ALG socket** 跟這套東西講話：
  `socket(AF_ALG)` → `bind()` 指定演算法 → `setsockopt(ALG_SET_KEY)` 設鑰匙
  → `sendmsg()` 送資料

### ⚠️ 一個現實的取捨

走 AF_ALG 要做好幾次系統呼叫，**比純使用者空間的 OpenSSL 慢**。
書上有做 1GB 檔案的計時比較（`openssl enc` vs `openssl enc -engine afalg`）。

> 📌 書上列出了測量指令，但 PDF 抽出的文字裡實際秒數被切掉了，
> 所以**我沒辦法引用具體數字**。要看的話翻書頁 13–14（PDF 33–34）。

### 工具：crypto-afalg

書作者用的工具，指令跟 openssl 幾乎一樣，但**走 kernel crypto API + keyring**。
之後所有需要「用 kernel 裡的鑰匙做事」的地方都是它。

如果它報 `socket(AF_ALG): Address family not supported`，檢查 kernel 設定：

```
CONFIG_CRYPTO_USER=y
CONFIG_CRYPTO_USER_API=y
CONFIG_CRYPTO_USER_API_HASH=y
CONFIG_CRYPTO_USER_API_SKCIPHER=y
```

### 埋一個伏筆

在 i.MX 的 `/proc/crypto` 裡，CAAM 會提供**兩個** AES-ECB 實作：
`ecb(aes)` 和 `tk(ecb(aes))`。同一個演算法，但**吃不同種類的鑰匙**。
`tk` = trusted key。這個差別到 §4、§5 才會完全講清楚。

> 📄 **原文**　書 p.5 ｜ PDF p.25
>
> [...] regarding the above encryption/decryption commands, we have to specify
> the key in the command line (or from a file), which exposes the key to everyone
> who has access to the root filesystem (with the right privileges, of course).
> In this book, we are going to see several ways to prevent the key from being read
> even if a process has the root privileges!

<!-- -->
> 📄 **原文**　書 p.18 ｜ PDF p.38
>
> The reader should notice in the above output that we have two different
> AES-ECB implementations supported by the CAAM [...]: one named ecb(aes) and the
> other named tk(ecb(aes)). What is crucial here is that we have the same AES-CBC
> algorithm, but it works on different keys!

📖 **書頁 5–18** ｜ PDF 頁 25–38 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=25)

---

## §3 鑰匙放哪裡：kernel keyring

### 這在解決什麼問題

鑰匙要待在 kernel 裡，那 kernel 得有個地方放它們、有辦法管它們。
這就是 **Linux Key-Management Facility**（也叫 Kernel Key Retention Service
或就叫 keyring）。

### 怎麼運作

用檔案系統來類比就很清楚：

- **key** = 檔案
- **keyring** = 資料夾（實際上 keyring 本身也是一種 key，只是它的內容是一串 key）

工具是 `keyctl`。兩個常用的特殊 keyring 代號：

| 代號 | 名字 | 生命週期 | 比喻 |
|---|---|---|---|
| `@s` | session keyring | 登入時建立，登出就沒 | 今天出門帶的錢包 |
| `@u` | user keyring | 綁 UID，跨登入 session 還在 | 銀行保險箱 |

常跑的服務、cron job 要用的長期鑰匙 → `@u`。
臨時的 → `@s`。

### 讀 `keyctl show` 的輸出

```
886145736 --alswrv  1000 1000  keyring: _uid.1000
311176563 --alswrv  1000 1000  user: userkey
^^^^^^^^^ ^^^^^^^^  ^^^^ ^^^^  ^^^^  ^^^^^^^
序號      權限      UID  GID   類型  描述/名字
```

權限字母：

- `v` view — 可以看類型、描述這些屬性
- `r` read — 可以讀出**內容本身**（payload）
- `w` write — 可以改內容
- `s` search — 搜尋 keyring 時找得到它
- `l` link — 可以被連到別的 keyring
- `a` alter — 可以改它的屬性（過期時間、權限）。算管理權限

> 📌 書上明說 keyring 本身「不在本書詳細講解範圍」。想深入看
> kernel 原始碼的 `Documentation/security/keys/`。

<!-- -->
> 📄 **原文**　書 p.18 ｜ PDF p.38
>
> The Linux Key-Management Facility, also known as the Linux Kernel Key
> Retention Service or Linux Keyring, is a core component of Linux that is
> primarily a way for various kernel components to retain or cache security data,
> authentication keys, encryption keys, and other data in the kernel.

<!-- -->
> 📄 **原文**　書 p.20 ｜ PDF p.40
>
> Readers can think of the session keyring (@s) as their wallet for a single
> day, while the user keyring (@u) is more like a permanent safety deposit box for
> a specific [user].

📖 **書頁 18–21** ｜ PDF 頁 38–41 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=38)

---

## §4 四種 key，安全性由低到高

### 這在解決什麼問題

「鑰匙放 kernel」聽起來安全，但還要問三個問題：

1. 鑰匙在 kernel 裡是**明文還是加密**的？
2. **使用者空間讀不讀得到**？
3. **重開機還在不在**？

四種 key 就是這三題的不同答案組合。

### 分類總表

| 種類 | kernel 裡是 | 使用者空間 | 重開機後 | 靠什麼保護 |
|---|---|---|---|---|
| **user** | 明文 | **讀得到** | 沒了 | 幾乎沒有 |
| **logon** | 明文 | **讀不到** | 沒了 | kernel 拒絕讀 |
| **trusted** | 明文 | 只拿得到封好的 blob | **還在**（存 blob） | 硬體信任源 |
| **encrypted** | 加密 | 只拿得到封好的 blob | **還在**（存 blob） | 另一把 master key |
| **CAAM（廠商專屬）** | **封好的** | 封好的 | **還在** | CAAM 硬體本身 |

### 4.1 明文 key：user 與 logon

書上把這兩種叫「plain text key」，因為它們在 kernel 裡是**沒加密**的。
（註：這是作者自己的分類用語，kernel 文件就叫它們 user 和 logon。）

**user key**：內容隨便你放，使用者空間可以建、可以改、**可以讀**。

```bash
keyctl add user userkey "key_data" @u
# padd 版本從 stdin 讀，等價
echo -n "key_data" | keyctl padd user userkey @u
```

**logon key**：關鍵差別 —— **使用者空間永遠讀不出來**。

```bash
echo -n "key_data" | keyctl padd logon logonkey: @u
keyctl pipe 779318636
# → keyctl_read_alloc: Operation not supported
```

而且**就算你把 read 權限加回去，還是讀不到**：

```bash
keyctl setperm 779318636 0x003f0000   # 全開
keyctl pipe 779318636
# → 還是 Operation not supported
```

這不是權限問題，是 key 的**類型**本身就不支援讀取。

> ⚠️ **logon key 的名字必須有冒號**，前面要有一段非空字串當「子類別」。
> 寫 `logonkey:` 或 `logonkey:testing` 都行，但不能只寫 `logonkey`。
> 這個冒號之後在 dm-crypt 的參數裡還會再出現一次（§5），別漏掉。

**實際用法**：把鑰匙塞進 logon key，之後就再也不用在命令列出現鑰匙了。

```bash
# 把 hex 字串轉成 binary
echo 0123...cdef | xxd -r -p > /tmp/key.bin
# 放進 logon key
keyctl padd logon cypher: @s < /tmp/key.bin
# 用它解密（鑰匙不出現在指令裡）
cat /tmp/secret.enc | crypto-afalg decrypt aes-256-cbc -k cypher:
```

從這一刻到重開機為止，這把鑰匙只有 kernel 知道。

> 用 key 名字（而不是序號）指定，需要 kernel **6.2 以上**
> （要有 `ALG_SET_KEY_BY_KEY_SERIAL`）。

**缺點**：重開機就沒了。這是下一節要解決的。

### 4.2 封起來的 key：trusted 與 encrypted

「**封（seal / wrap）**」是這本書最重要的一個動作，先講清楚：

> **封** = 把鑰匙用另一個東西加密成一坨看不懂的資料（blob）。
> 這坨 blob 可以隨便存在磁碟上，因為只有「封它的那個東西」能解開。

兩種 key 的差別就在「封它的是誰」：

- **trusted key**：靠**硬體信任源**封。可用的信任源有：
  - **TPM** — 專用安全晶片。亂數品質看廠商
  - **TEE / OP-TEE** — 基於 ARM TrustZone 的可信執行環境
  - **CAAM** — NXP i.MX 上的加密硬體，有硬體亂數產生器
  - **DCP** — 部分 i.MX 的加密加速器，**沒有自己的亂數源**，用 kernel 預設的

  對應的 kernel 設定：`CONFIG_TRUSTED_KEYS_TPM` / `_TEE` / `_CAAM` / `_DCP`。
  kernel 挑第一個可用的，也可以用 kernel command line 指定
  `trusted.source=tpm`（或 `tee` 等）。亂數源可以用 `trusted.rng=kernel` 蓋掉。

- **encrypted key**：靠**另一把 trusted key**（叫 **master key** 或 **KMK**，
  Kernel Master Key）封。因為不用碰硬體，所以**比較快**。

還有一個差別：trusted key **一定是亂數**；encrypted key 可以是亂數，
也可以由使用者指定內容（需要 `CONFIG_USER_DECRYPTED_DATA`，否則會噴
`add_key: Invalid argument`）。

### trusted key 怎麼運作（重要）

```
建立：keyctl add trusted trustedkey "new 32" @s
      → 信任源產亂數 → 鑰匙以【明文】放在 kernel 裡

匯出：keyctl pipe <serial> > trustedkey.blob
      → 鑰匙被信任源封成 blob → 存到磁碟

重開機

還原：keyctl add trusted trustedkey "load $(cat trustedkey.blob)" @s
      → 信任源解開 blob → 鑰匙又以【明文】回到 kernel
```

（書上 Figure 1-1）

**這就是「跨重開機還在」的作法**：鑰匙本身沒存，存的是封起來的 blob。

> ⚠️ **重開機前一定要先把 blob 存到非揮發性儲存**，不然鑰匙就真的沒了。

**兩層疊起來用**（書上的實際流程）：

```bash
# 1. 先載入 master key（trusted）
keyctl add trusted trustedkey "load $(cat trustedkey.blob)" @s
# 2. 再載入被它封的 encrypted key
keyctl add encrypted encryptedkey "load $(cat encryptedkey.blob)" @s
# 3. 用它解密，鑰匙全程沒進使用者空間
crypto-afalg decrypt aes-256-cbc -k encryptedkey < message.enc
```

> 🔒 因為 trusted key 綁硬體，**加密的訊息只能在同一台機器上解開**。
> 這正是 §0 講的「防複製」怎麼做到的。

### 4.3 廠商專屬 key：CAAM

**CAAM** = Cryptographic Acceleration and Assurance Module，
NXP 很多 i.MX CPU 上的加密硬體。工具是 NXP 的 `caam-keygen`
（<https://github.com/nxp-imx/keyctl_caam>）。

```bash
caam-keygen create caamkey ecb -s 32   # 產一把 256-bit 的鑰匙
```

### 🎯 CAAM key 和 trusted key 的關鍵差別

這是第 1 章最重要的一句話，**書上書頁 46（PDF 66）用驚嘆號強調**：

> **trusted key**：明文的鑰匙**在 kernel 裡**，封起來的版本在磁碟上。
> **CAAM key**：明文的鑰匙**在 CAAM 硬體裡**，
> 移到 kernel 的時候就**已經是封好的**了。

換句話說：用 trusted key，攻破 kernel 就拿得到鑰匙明文。
用 CAAM key，攻破 kernel 也只拿得到封好的 blob。**多擋一層**。

（書上 Figure 1-1 vs Figure 1-2，兩張圖裡都有個叫 `key` 的變數，
但裝的東西不一樣——這是作者特別提醒的點。）

> 📄 **原文**　書 p.31 ｜ PDF p.51
>
> By using the term sealed, we mean such keys that are created in the kernel,
> and user space sees, stores, and loads only encrypted blobs. [...] Furthermore,
> these keys are persistent across reboots, unlike the logon keys, which vanish on
> a reboot.

<!-- -->
> 📄 **原文**　書 p.46 ｜ PDF p.66
>
> Now, within the caamkey file, a new 256-bit key is stored, and it is known by
> the CAAM only! This is a similar situation as per trusted keys; however, there is
> a crucial difference! While a trusted key is stored in its unsealed form in the
> kernel, a CAAM key is stored in its unsealed form in the CAAM. When it is moved
> to the kernel, it is sealed (see Figure 1-2).

📖 **書頁 21–47** ｜ PDF 頁 41–67 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=41)

---

## §5 磁碟加密兩條路

### 這在解決什麼問題

前面都在講「一把鑰匙」。但實際上要保護的是**整個檔案系統**。
而且必須**透明**——程式讀寫檔案時完全不用改，加解密由 kernel 自動做。

這叫 **transparent encryption**：資料在磁碟上（at rest）是加密的，
但對執行中的作業系統和程式來說看起來就是明文。

### 兩種作法

```
    檔案系統層                        區塊層
   （fscrypt / eCryptfs）           （dm-crypt）
   ┌─────────────┐                 ┌─────────────┐
   │ 應用程式     │                 │ 應用程式     │
   ├─────────────┤                 ├─────────────┤
   │ 檔案系統     │← 這層做加解密    │ 檔案系統     │
   ├─────────────┤                 ├─────────────┤
   │ 區塊裝置     │                 │ dm-crypt    │← 這層做加解密
   └─────────────┘                 ├─────────────┤
                                   │ 區塊裝置     │
   可以只加密某些目錄                └─────────────┘
                                   整顆一起加密
```

（書上 Figure 1-3）

### 檔案系統層（書頁 48–63｜PDF 68–83）

好處是**粒度細**——可以只加密某幾個檔案或目錄。兩種實作方式：

- **stacked（疊在上面）**：例如 **eCryptfs**（kernel module）、
  **EncFS**、**gocryptfs**（後兩者基於 FUSE）。
  下層檔案系統看到的是正常檔案，只是內容是密文。
  > ⚠️ 書上明說 **eCryptfs 已經沒在維護，不要用在正式產品**。
- **native（檔案系統自己支援）**：EXT4、F2FS、UBIFS 都支援。
  現在比較主流，因為不用疊一層、比較省記憶體、設定也不一定要 root。

一個實用細節：把 key 從 keyring 移除**不夠**，因為 kernel 會快取。
真的要鎖上，兩個都要做：

```bash
keyctl unlink <serial> @s
sync && echo 3 > /proc/sys/vm/drop_caches
```

### 區塊層：dm-crypt（書頁 63–75｜PDF 83–95）← 這本書用的

在**區塊裝置**這層做。做出一個虛擬的加密區塊裝置，然後在上面
格式化一般的檔案系統。

```bash
dmsetup create root --table \
  "0 $SECTORS crypt aes-cbc-plain $KEYHEX 0 /dev/loop0 0"
```

參數逐個是：

| 位置 | 值 | 意思 |
|---|---|---|
| 1 | `0` | 從第幾個 sector 開始加密 |
| 2 | `$SECTORS` | 磁碟總長度（以 512-byte sector 計） |
| 3 | `crypt` | target 類型，固定 |
| 4 | `aes-cbc-plain` | 演算法 + IV 模式（見下） |
| 5 | `$KEYHEX` | 鑰匙 |
| 6 | `0` | IV 的偏移量；用 `-plain` 時固定 0 |
| 7 | `/dev/loop0` | 底下真正的區塊裝置 |
| 8 | `0` | 在該裝置上的起始偏移 |

`-plain` 的意思：**用 sector 編號當 IV**（32-bit little-endian，不足補零）。
好處是同樣內容的不同 sector 加密結果不同，而且不用去磁碟上另外讀 IV，比較快。

做完會出現 `/dev/mapper/root`，可以像一般裝置那樣 `mkfs.ext4`。

### 🎯 為什麼開機訊息裡是 `/dev/mapper/root`

這解答了 §9 會看到的一件事：

```
init: mounting rootfs on /dev/mapper/root...
```

不是 `/dev/mmcblk2p4`，是 `/dev/mapper/root`——因為中間隔了一層 dm-crypt。

### 用 CAAM key 做 dm-crypt（最高安全等級）

```bash
caam-keygen create caamkey ecb -s 16
keyctl padd logon caamkey: @s < /etc/caam/caamkey
dmsetup create root --table \
  "0 $SECTORS crypt capi:tk(cbc(aes))-plain :36:logon:caamkey: 0 /dev/loop0 0"
```

兩處改動要注意：

- `capi:tk(cbc(aes))-plain` — 要用 **`tk(...)`** 這個演算法名字
  （tk = trusted key），kernel 才知道要用特殊方式處理這把鑰匙。
  **這就是 §2 埋的那個伏筆**。
- `:36:logon:caamkey:` — logon key 的描述前面要有非零長度的子類別字串，
  所以**最後那個冒號不能漏**。`36` 是這把 key 的位元組長度。

> 📌 如果需要做**預先建好的 rootfs 映像檔**（產線用），可以用 `-t`
> 指定一把已知的 CAAM key：`caam-keygen create caamkey ecb -t 0123...cdef -h`

<!-- -->
> 📄 **原文**　書 p.47 ｜ PDF p.67
>
> Transparent encryption in Linux refers to a method of protecting data on a
> storage device with the help of the kernel. In fact, the encryption and
> decryption happen automatically and on-the-fly. So the data is always encrypted
> when at rest (on the disk) but appears as plain text to the running operating
> system and its users when accessed. This approach allows user-space applications
> to work as if everything were in plain text.

📖 **書頁 47–75** ｜ PDF 頁 67–95 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=67)

---

# 第二部分：Secure Boot 是什麼（第 2 章）

---

## §6 信任鏈是什麼

### 這在解決什麼問題

Secure Boot 想解的問題：**確保只有合法的軟體能在合法的硬體上跑，
而且反過來也成立。**

具體來說，它要防三件事：

1. 未授權的軟體被執行（bootloader、kernel，某種程度上還有使用者程式）
2. **系統被複製**——把合法軟體抓出來，灌到山寨硬體上跑
3. **關機狀態下祕密被讀走**

### 怎麼運作：一棒接一棒

```
ROM code ──驗──> SPL ──驗──> U-Boot + OP-TEE ──驗──> kernel ──解密掛載──> rootfs
   ↑
Root-of-Trust
（無條件相信）
```

每一棒的動作固定是三步：**驗簽章 → 解密 → 執行**。

**Root-of-Trust（信任的根）** 是起點。它沒有人驗它——它的安全性
是「假設」出來的，因為它被物理或邏輯上保護著。通常就是**燒死在晶片裡的
ROM code**，改不了。

ROM code 用來驗第一棒的公鑰通常放在晶片的 **fuse**（或其他非揮發性記憶體）裡。

### 每一棒的鑰匙可以不一樣

書上說：每個階段用不同的鑰匙，信任鏈**更穩固**；但即使每個階段都用同一組鑰匙，
這個機制**依然被認為是穩固的**。

### 可以加上的強化：tamper detection

如果簽章無效、缺失，或**硬體被動過**（例如外殼被打開），
Secure Boot 會擋下開機並通常會告警。

> 📌 細節在附錄 A，**不在這輪筆記範圍**。

<!-- -->
> 📄 **原文**　書 p.79 ｜ PDF p.98
>
> Each piece of boot software from the bootloaders (and their companion
> software), the kernel, and the rootfs must be digitally signed and encrypted with
> several private keys. The first component, the fundamental one, is the one that
> is trusted by default, and it is called Root-of-Trust. The Root of Trust cannot be
> verified by anything else in the system; its security is assumed because it is
> physically or logically protected. Usually, this is the ROM code fused into the
> chip.

<!-- -->
> 📄 **原文**　書 p.81 ｜ PDF p.100
>
> For each stage, keys may change, and, in this case, the Chain-of-Trust is
> more robust; however, this mechanism is considered robust even in the case where
> we decide to use the same keys in each stage.

📖 **書頁 79–82** ｜ PDF 頁 98–101 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=98)

---

## §7 信任鏈的破口：rootfs

### 🎯 這是全書最重要的一個「不保護」

信任鏈到 rootfs 這一棒**性質變了**：

> **rootfs 只有加密，沒有簽章。**
> 所以最後這一棒的安全性，**完全只靠加密鑰匙**。

### 為什麼不能簽 rootfs

因為簽章的程序**沒有加密那麼有效率**。加密磁碟是用「單一區塊加密」
一次做完的，簽章沒辦法這樣做。

### 後果

一旦加密的 rootfs 掛載完成：

> 從行程的角度看，它就是一個**普通的、沒有加密的**檔案系統。
> 沒有人再檢查裡面每一支程式的有效性——**包括 `/sbin/init` 本身**。

換句話說：信任鏈保證的是「**整個檔案系統**是對的」，
不是「裡面**每支程式**是對的」。

### 書上給的補救方向

**Linux IMA**（Integrity Measurement Architecture），
<https://sourceforge.net/p/linux-ima/wiki/Home/>

> 📌 書上明說 **IMA 不在本書涵蓋範圍**。這是你之後想補強時的第一個方向。

<!-- -->
> 📄 **原文**　書 p.81 ｜ PDF p.100
>
> As the last step, the kernel, by using an encryption key, mounts the real
> rootfs. Readers should notice that in this last step the security is given by the
> encryption key only, since it's not possible to have a signed rootfs!
> [...] the signature procedure is not as efficient as the encryption one. [...] an
> encrypted disk is implemented by doing a single block encryption, and this
> operation cannot be done for signing.

<!-- -->
> 📄 **原文**　書 p.78 ｜ PDF p.97
>
> Moreover, we should consider that once the encrypted rootfs is mounted, from
> the process perspective it is a normal rootfs (with no encryption), so the rootfs
> encryption is an effective protection when the system is in the powered-off
> state!

📖 **書頁 81、96** ｜ PDF 頁 100、115 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=100)

---

## §8 Secure Boot 不做的事

### 這在解決什麼問題

避免你對它有錯誤期待。書上花了整整一節在講這個。

### Secure Boot 的工作範圍

> 從開機的那一刻開始，到**加密的 rootfs 掛載完成**為止。
> 作業系統跑起來之後，Secure Boot 就下班了。

### 它**不**保護的東西

- ❌ 病毒、勒索軟體、間諜軟體、釣魚——這些都是系統跑起來之後的事
- ❌ DDoS、中間人攻擊、任何網路攻擊
- ❌ **執行中的 rootfs**。rootfs 加密只在**關機狀態**有意義

所以還是需要防火牆、還是要小心你下載執行什麼、還是要備份。

### 書上的比喻

> Secure Boot 是站在電腦開機流程入口的**一個很專門的警衛**。
> 它的工作是確保只有受邀且驗證過的客人（簽過章的開機軟體）能進來。
>
> **它是一層地基，不是一整套安全方案。**

<!-- -->
> 📄 **原文**　書 p.78 ｜ PDF p.97
>
> [Secure Boot] is strictly designed to protect the boot process by verifying
> the integrity of the software before the operating system fully loads. Its job is
> about verifying the integrity and authenticity of boot components until the mount
> of the encrypted rootfs. Once the operating system is up and running, Secure
> Boot's job is done.

<!-- -->
> 📄 **原文**　書 p.79 ｜ PDF p.98
>
> The Secure Boot is a very specific guard, positioned right at the entrance of
> our computer's boot process. Its job is to make sure that only invited and
> verified guests (signed boot software) are allowed into the system, preventing
> unauthorized or malicious entities from getting in before anything else starts.
> It's a foundational security layer, not a comprehensive security suite!

📖 **書頁 77–79** ｜ PDF 頁 96–98 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=96)

---

## §9 開機流程，一棒一棒看

### 這在解決什麼問題

把 §6 那條抽象的鏈，對到真實開機訊息上。

> ℹ️ 書上 Figure 2-2 是以 **ARM 系統**為準（所以有 TF-A、OP-TEE
> 這些 ARM 專屬的東西）。但稍作調整後，可以當成一般 Linux 開機流程的概觀。

### 全景

```
上電
 │
 ├─ 1. ROM boot code          ← 燒死在晶片，唯一無條件安全的東西
 │      驗簽 SPL
 ├─ 2. SPL（prebootloader）    ← 初始化 DRAM
 │      /  TF-A → 載入 U-Boot + OP-TEE
 ├─ 3. U-Boot（Normal World）  ← 加上 OP-TEE（Secure World）
 │      驗簽 + 解密 fitimage
 ├─ 4. kernel                 ← 從 fitimage 裡出來
 │      掛 initramfs
 ├─ 5. initramfs 的 init      ← 解密、掛載真正的 rootfs
 │      switch_root
 └─ 6. 真正的 rootfs + systemd
```

### 第 1 棒：ROM code

上電後 ROM code 先跑，做完初始化，從儲存裝置載入 bootloader
（或 prebootloader）並執行。

因為它是**預先燒進 ROM 晶片**的指令，改不了，
所以**它是唯一被認為安全的元件**（從 Secure Boot 的角度）。

其他每一個元件都必須被保護。

### 第 2 棒：為什麼需要 SPL

**因為 DRAM 剛上電時不能用。**

現代系統用的動態記憶體（DRAM）在上電時是未初始化的原始狀態。
CPU 沒辦法把程式載進去、也不能在裡面執行程式，
除非先設定好 DRAM 控制器和 DRAM 晶片本身（時序、refresh rate、電壓等）。

所以需要一個小小的 **prebootloader** 先把 DRAM（和其他必要硬體）弄好，
之後比較大、比較複雜的程式（真正的 bootloader，有些系統甚至是 kernel 本身）
才能被載進去執行。

在這本書裡：**prebootloader = U-Boot SPL**（Secondary Program Loader），
**bootloader = U-Boot**。

（如果某個系統的 DRAM 一上電就能用，ROM code 就可以直接載 bootloader。）

### 第 2.5 棒：TF-A 和 OP-TEE

現代 ARM 系統在這一步還會多兩個元件：

**TF-A**（Trusted Firmware-A，也叫 ATF、ARM Trusted Firmware）
- 給 ARMv8-A / ARMv9-A 用的關鍵韌體
- 跑在**最高權限等級**，扮演 **secure monitor**
- 從我們的角度看，它的主要任務是：**載入 U-Boot 和（選配的）OP-TEE 並執行它們**
- 文件：<https://trustedfirmware-a.readthedocs.io/>

**OP-TEE**（Open Portable Trusted Execution Environment）
- 用 ARM **TrustZone** 技術，把**一顆實體 CPU 切成兩個隔離的世界**：

| | Secure World | Normal World |
|---|---|---|
| 誰在裡面 | OP-TEE（TEE） | Linux（REE） |
| 保護 | 硬體級保護，就算 Normal World 被攻破也安全 | 可存取大部分系統資源 |
| 能不能碰對方 | 可以 | **不能**存取或竄改 Secure World |

- 隔離靠的是：硬體強制的記憶體隔離、受保護的暫存器、
  受控的進出點（透過 secure monitor，通常就是 TF-A 實作的）
- 很常見的情況是 **OP-TEE 跑在同一顆晶片裡的另一顆 CPU 上**
- 文件：<https://optee.readthedocs.io/>

在 Secure World 裡跑的程式叫 **Trusted Application（TA）**。

**分工**：OP-TEE 待在它的 Secure World 裡；U-Boot 在 Normal World 做設定，
然後載入並執行 kernel，過程中**需要加密幫忙時就去問 OP-TEE**。

### 實際開機訊息：SPL 階段

```
U-Boot SPL 2024.04-imx_...
DDRINFO: start DRAM init          ← 這就是 SPL 在初始化 DRAM
DDRINFO: DRAM rate 4000MTS
DDRINFO: ddrphy calibration done
Normal Boot
Trying to boot from BOOTROM
Authenticate image from DDR location 0x401fadc0...   ← 🎯 驗簽在這裡
NOTICE:  ...                       ← NOTICE 開頭的都是 OP-TEE 印的
```

ROM code 驗完 SPL 之後，接著驗 U-Boot 和 OP-TEE 的映像檔。

### 實際開機訊息：U-Boot 階段

```
U-Boot 2024.04-imx_...
Model: board i.MX8MPlus iCore Plus
Loading Environment from MMC... OK
Hit any key to stop autoboot:
...
75301040 bytes read in 238 ms (301.7 MiB/s)
Booting from mmc ...
```

### ⚠️ 一個容易誤解的點：bootloader 可以不加密

書上的例子裡，**bootloader 只有簽章，沒有加密**。

為什麼可以？因為：

- 有簽章 → **信任鏈沒有斷**
- bootloader 裡沒有敏感資訊 → 就算是明碼，那也只是 bootloader 的程式碼，
  不是應用程式

**但是**（書上用警告框強調）：

> 如果 bootloader 裡**有**祕密（加密鑰匙、密碼），
> 那就必須整個加密，或至少把那段關鍵資訊雜湊或封起來。
> **否則信任鏈就斷了！**

### 第 3 棒：fitimage

當 U-Boot 找到有效的 **fitimage** 時：

> **fitimage** = 一個檔案，裡面包了 kernel image、Device Tree（DTB）、
> 還有其他開機需要的資訊。

```
Booting from mmc ...
Authenticate image from DDR location 0x40400000...   ← 🎯 又一次驗簽
Secure boot enabled
HAB Configuration: 0xcc, HAB State: 0x99
No HAB Events Found!
## Loading kernel from FIT Image at 40400000 ...
## Loading fdt from FIT Image at 40400000 ...
Starting kernel ...
```

U-Boot **先驗 fitimage 的簽章，再解密它**，然後執行。
看到 `Starting kernel ...` 就代表 CPU 開始跑 Linux 的程式碼了。

（`HAB` = NXP 的 High Assurance Boot。書上沒展開解釋這個名詞。）

### 第 4 棒：kernel command line

kernel 起來後，設定所有元件和裝置，然後做最後兩件事：
**掛載 rootfs**、**執行 init**。

bootloader 用 **kernel command line** 跟 kernel 交換資訊——
想像成 bootloader 是「用一行命令列」在執行 kernel：

```
Kernel command line: console=ttymxc1,115200 device=/dev/mmcblk2
  root=/dev/mmcblk2p4 rootwait rw initramfs_normal
  boot_schema=a_b root_name=root_b
```

等同於在 U-Boot 下打：

```
uboot> fitimage console=ttymxc1,115200 device=/dev/mmcblk2 \
       root=/dev/mmcblk2p4 rootwait rw initramfs_normal \
       boot_schema=a_b root_name=root_b
```

這些參數的意思在 §13 會用到（`boot_schema` 決定用哪種分割區配置）。

> 📌 **這裡有個安全問題**：U-Boot 的環境變數是**明文**的記憶體區域。
> 書上把「怎麼保護這些資訊」放在**附錄 B**，**不在這輪筆記範圍**。

### 第 5 棒：initramfs 和 switch_root

**rootfs** 是 Linux 檔案系統階層的最頂層，就是那個 `/`。
所有其他檔案和目錄都掛在它下面。

kernel 可以直接掛載儲存裝置上的 rootfs，但現代系統偏好中間多一步：

> **initramfs** = 一個小小的、暫時的、**在記憶體裡**的 root filesystem。
> 想成一個自給自足的迷你作業系統，唯一的任務就是幫真正的作業系統起床。

它可以放在儲存裝置上，但**很常見的是直接包在 kernel 裡面**
（所以 fitimage 裡有它）。

**什麼時候需要 initramfs**：真正的 rootfs 不能被 kernel 直接存取的時候。
例如 rootfs 在 RAID 上、或**需要先解密**、或要先更新整個 rootfs。

做完該做的事之後，initramfs 裡的 init 用 `switch_root` 切過去：

```bash
exec switch_root /real_rootfs /sbin/init
```

### 🎯 兩個容易搞錯的細節

**(1) `switch_root` ≠ `chroot`**

| | `switch_root` | `chroot` |
|---|---|---|
| 影響範圍 | **整個 kernel 的 root filesystem** | 只有那個行程和它的子行程 |
| 用途 | 開機時從暫時 root 換到永久 root | 隔離環境（編譯、修復系統、daemon） |
| 舊的 root | **遞迴刪除**、搬移、隔離掉 | 完全不動 |

`switch_root` 會把 `/proc`、`/dev`、`/sys`、`/run` 搬到新的 root，
把新的 root 變成系統的 root，然後啟動 init。

**為什麼要遞迴刪掉舊的 root**：
- initramfs 佔的是 RAM，內容已經不需要了，刪掉可以回收
- **更重要**：它可能藏著我們**不想讓真正的 rootfs 看到的資訊**（例如鑰匙）

**(2) 為什麼一定要 `exec`**

在 shell 裡：

- `<cmd>` → shell fork 出新行程，然後等它結束
- `exec <cmd>` → **shell 本身變成 `<cmd>`**。不產生新行程，
  shell 的 PID 被 `<cmd>` 取代，shell 永遠不會回來

為什麼這很關鍵？因為**真正 rootfs 裡的 init 必須是 PID 1**
（正常運作的 init 就該是 PID 1）。

### 開機訊息：切換的那一刻

```
init: checking rootfs on /dev/mapper/root...
e2fsck 1.47.0 (5-Feb-2023)
root: clean, 17913/256000 files, 228590/1024000 blocks
init: mounting rootfs on /dev/mapper/root...
init: entering rootfs on /dev/mapper/root...
```

注意 **`/dev/mapper/root`**——不是一般的 `/dev/sda1` 或 `/dev/mmcblk2`，
而是實作 rootfs 加密的特殊區塊裝置。**這就是 §5 講的 dm-crypt**。

接著 initramfs 的 init 被真正的 init（例子裡是 systemd）取代，開機完成。

> 📄 **原文**　書 p.83 ｜ PDF p.102
>
> Modern systems use dynamic RAM (DRAM), which is not ready to be used at
> power-on. It's an uninitialized raw state, and the CPU cannot simply [load and
> execute code in it before the DRAM controller and the DRAM chips themselves have
> been set up].

<!-- -->
> 📄 **原文**　書 p.91 ｜ PDF p.110
>
> An initramfs is a small, temporary, in-memory root filesystem that the Linux
> kernel uses during its early boot stages, before the real root filesystem (the
> one containing our entire operating system) can be mounted. Think of it as a
> small, self-contained mini-operating system whose sole purpose is to help the
> main operating system get started.

📖 **書頁 82–96** ｜ PDF 頁 101–115 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=101)

---

## §10 板子出廠：自家工廠 vs 代工廠

### 這在解決什麼問題

前面講的都是「系統正常運作」的狀態。但每個系統都有**產線階段**——
板子剛組裝好，是一張白紙，什麼都沒有。

要往裡面灌東西（叫 **firmware programming** 或 **flashing**），
而 Secure Boot 讓這件事變複雜了。

### 產線要做的事

1. 所有韌體映像檔必須**簽好章**、（最好也）**加密**。
   只有不敏感的資料可以是明文或不簽
2. 把 CPU 設定成進入**安全狀態**
3. 把簽章鑰匙和（最好還有）加密鑰匙**燒進 CPU 的 fuse**

這一整套最佳實務叫 **SSP**（Software Secure Provisioning）。

### 情境 A：自家工廠（書頁 98–99｜PDF 117–118）

流程：

1. CPU 做一般開機，透過**序列埠或 USB** 載入初始程式碼
   （通常是一個特別設定的 U-Boot）
2. 初始程式碼把需要的鑰匙**燒進 fuse**，並檢查一切正常
3. 沒問題就把初始韌體寫進 flash，然後重開機
4. CPU 現在以**安全狀態**執行，載入安全的 bootloader，信任鏈開始運作

**步驟 1 可以用沒簽章的 bootloader**——因為是我們自己做的，
可以假設沒有惡意軟體。

**⚠️ 步驟 2 比較麻煩**：關鍵鑰匙會經過通訊通道。
序列匯流排**用便宜的儀器就能監聽**。

**解法：Diffie–Hellman 金鑰交換協定**
讓兩個原本互不認識的人，在不安全的通道上**談出一把共用的祕密鑰匙**。
（書上 Figure 2-3）

**這個作法幾乎所有 CPU 都能實作。真正的風險點是：
fuse 燒錄過程中不能有惡意的軟體或硬體在偷。**

### 情境 B：代工廠（書頁 100–102｜PDF 119–121）

情境 A 的假設在這裡**全部不成立**。

就算用了金鑰交換協定，也有兩個沒法保證的事：

1. 步驟 1 執行的初始程式碼，**真的是我們給的那份嗎？**
2. 就算程式碼是對的，**它跑在真的板子上、還是假裝成板子的偷鑰匙機器上？**

書上的具體情境：

> 我們給代工廠一套特製硬體，開機時把我們的程式送進每片新板子。
> 然後我們用同一套系統跟新裝置通訊，把要燒進 fuse 的鑰匙送過去。
>
> **但誰能保證我們對話的對象是真的新裝置，
> 而不是模仿通訊協定、只想偷鑰匙的惡意硬體？**

**唯一的解法：在 ROM code 裡做身分驗證。**

因為 ROM code 預設是安全的，所以可以靠 CPU 廠商提供的**憑證**
來確認對面是真貨。

流程：

1. 目標 CPU 做受保護的開機，ROM code 送出**帶公鑰的憑證**
2. 主機用 CPU 廠商的公鑰（當作 CA）驗證憑證，通過就回送自己的公鑰
3. 用產生的共用鑰匙建立安全通道，主機安全地把鑰匙送給目標的 ROM code，
   ROM code 去燒 fuse
4. 燒完重開機進安全狀態，產線繼續

（書上 Figure 2-4）

### ⚠️ 兩個限制

- 這個流程**需要 CPU 特別支援，不是所有 CPU 都做得到**
- 書上提到還有另一種解法：先用一個**已簽章的 bootloader** 去寫 fuse
  的前置階段。但**明說「不在本書範圍」**

> 📄 **原文**　書 p.97 ｜ PDF p.116
>
> Firstly, we should consider that all the firmware images must be properly
> signed and (hopefully) encrypted. Only nonsensible data can be in a plain text
> form or not signed. Then we must also program the CPU to enter into its secure
> state, and then the proper signature key and (hopefully) encryption key must be
> fused too within the CPU itself. All these best practices are commonly named
> Software Secure Provisioning (SSP).

<!-- -->
> 📄 **原文**　書 p.100 ｜ PDF p.119
>
> Well, but who can assure us that we're actually communicating with a new
> device and not with malicious hardware that, by mimicking the communication
> protocol, is simply trying to steal our keys? The only option is to use an
> authentication system within the ROM code! In fact, the ROM code is considered
> secure by default, and by using a special certificate provided by the CPU vendor,
> we can be sure that we are effectively speaking with a genuine system.

📖 **書頁 97–102** ｜ PDF 頁 116–121 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=116)

---

## §11 第一次開機才生出加密 rootfs

### 這在解決什麼問題

信任鏈要求所有映像檔都簽好、加密好。那能不能直接做一個
**預先建好的二進位 flash 映像檔**，產線直接灌進去就好？

**bootloader 和 kernel 可以。但加密的 rootfs 不行。**

### 為什麼不行

兩個原因：

1. **rootfs 是用隨機鑰匙加密的**——這把鑰匙通常**連開發者自己都不知道**
   （見 §5）
2. 就算你知道鑰匙，在某些 CPU 上這把鑰匙是**封起來（sealed）**的，
   而封裝的動作**每顆 CPU 產出的結果都不一樣**
   （因為封裝依賴每顆 CPU 獨有的 master key）

所以不可能預先做一份大家通用的加密 rootfs 映像檔。

### 解法：出一包 tar，第一次開機才解開

**產線灌進去的 flash 映像檔內容**（書上 Figure 2-5）：

| 檔案 | 狀態 | 放哪 |
|---|---|---|
| bootloader 映像檔 | 簽章 +（最好）加密 | **不放在分割區裡**，寫在磁碟的特定偏移位置 |
| `fitimage` | **簽章 + 加密**（兩個都要） | boot 分割區 |
| `rootfs.tar.zip.enc` | 簽章 + 加密的 TAR 壓縮檔 | factory 分割區 |
| `rootfs.signature` | 上面那包的數位簽章 | 同上 |

> 簽章也可以直接附在檔案後面，那就叫 `rootfs.tar.zip.enc.sign`。

**fitimage 裡的 kernel 又包了 initramfs，而 initramfs 裡放著兩把鑰匙**：

- `factory.enc.key` — 解開 factory rootfs 的**加密鑰匙**
- `rootfs.sign.key` — 驗證 factory rootfs 的**簽章公鑰**

### 開機流程

```
bootloader 載入、驗證、執行 fitimage
   ↓
fitimage 裡的 kernel 啟動，執行內嵌 initramfs 的 init
   ↓
init 用 rootfs.sign.key 驗證 rootfs 的簽章
   ↓ 通過
用 factory.enc.key 解密，建立新的加密 rootfs 分割區，把檔案裝進去
```

### 🎯 所以 fitimage 一定要加密

現在應該很清楚為什麼：

> **解開 rootfs TAR 檔的加密鑰匙就藏在 fitimage 的 initramfs 裡。**
> fitimage 不加密 = 鑰匙裸奔。

### 產生出來的鑰匙存哪

拿來產生加密 rootfs 的那把鑰匙，以**封起來（sealed）的形式**
存在 `/factory` 分割區（或任何明文分割區），供之後每次開機使用。

> 這裡不會有問題，因為**產生和封裝都是由實際要用它的那顆 CPU 自己做的**，
> 不是在某台通用主機上做的。

<!-- -->
> 📄 **原文**　書 p.103 ｜ PDF p.122
>
> We have seen in "The Block-Level Encryption" section in Chapter 1 that
> usually the rootfs is encrypted with a random key, which usually is not known to
> the developers either! So, it's obvious that we cannot prebuild a valid image for
> it. Furthermore, even if we perfectly know the encryption key, there is still the
> difficulty that on some CPUs this key is often sealed, and this operation
> produces different binaries for each CPU. [...] To address this issue, the best
> thing to do is to provide an initial root filesystem as a simple archive
> (typically a compressed TAR), and during the first boot, the system automatically
> creates the encrypted rootfs and copies all files into it.

📖 **書頁 103–105** ｜ PDF 頁 122–124 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=122)

---

## §12 更新系統要注意什麼

### 這在解決什麼問題

每個嵌入式產品都要能更新自己。有 Secure Boot 之後，更新要多注意幾件事
（不過比產線那邊寬鬆一些）。

### 更新包的內容（書上 Figure 2-6）

| 檔案 | 說明 |
|---|---|
| `bootloader.enc.sign` | bootloader（如果需要更新的話） |
| `fitimage.enc.sign` | kernel + DTB + initramfs |
| `rootfs.tar.zip.enc` | 加密壓縮的 rootfs |
| `rootfs.signature` | 上面那包的簽章 |

**全部都要用正確的鑰匙簽好、加密好**，否則更新會失敗，
更糟的情況是**系統直接掛掉**。

### 🎯 難點：兩把鑰匙

要更新 rootfs，需要拿到兩把鑰匙：

1. **解開更新包 TAR 檔的加密鑰匙**
2. （某些情況下）**目前執行中的 rootfs 的加密鑰匙**

第 2 把**不是問題**——它以封起來的形式存在 `/boot` 目錄裡。

第 1 把**比較麻煩**：怎麼取得它，又不讓它裸露在檔案系統上？

> 📌 書上說：這取決於你怎麼實作系統，等講到不同的開機方案（§13）
> 就會清楚。**現階段只要記住這把鑰匙必須妥善管理，防止被讀取。**

<!-- -->
> 📄 **原文**　書 p.105 ｜ PDF p.124
>
> Firstly, all firmware images must be properly signed and encrypted with the
> right keys, or the update may fail or, worse, the system will hang! A typical
> update can be an archive composed of the bootloader image (bootloader.enc.sign,
> if needed), the fitimage image (fitimage.enc.sign), and the rootfs as a
> compressed TAR archive (again as two separate files: rootfs.tar.zip.enc the
> compressed and signed image archive, and rootfs.signature the rootfs digital
> signature).

📖 **書頁 105–107** ｜ PDF 頁 124–126 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=124)

---

# 第三部分：兩種分割區配置（第 3 章，只講概念）

---

## §13 Rescue 方案 vs A/B 方案

### 這在解決什麼問題

Linux 裝在很多地方——桌機、手機、Wi-Fi AP、智慧電視，
還有火車、配電箱、醫療設備。

**後面那幾種，必須能在沒有人（或只有很少的專業支援）介入的情況下
可靠地還原和更新。** 所以所有元件在儲存裝置上怎麼擺，很重要。

### 前提：儲存裝置

現在最常用的是 **eMMC**（embedded MultiMediaCard）。

> **eMMC** = NAND flash + 控制器 + 介面，包在一個晶片裡。
> 跟裸 NAND 的差別就是它自帶控制器，所以對使用者來說**用起來就像硬碟**。

也還會看到 NOR、NAND，或混用（NOR + eMMC / NAND + eMMC）。

> 📌 另外還有 **RPMB**（Replay-Protected Memory Block，
> 例如 `/dev/mmcblk2rpmb`），是另一塊可以安全存放敏感資料的區域。
> **書上明說「不在本書範圍」**，只給了 OP-TEE 的文件連結。

### 分割區有哪些

| 分割區 | 掛在 | 放什麼 | 加密? |
|---|---|---|---|
| **boot** | `/boot` | fitimage（kernel + DTB + initramfs） | ❌ 明文 |
| **factory** | `/factory` | 廠商的關鍵資訊，可能還有完整的出廠 OS | ❌ 明文 |
| **root** | `/` | rootfs | ✅ **唯一加密的** |
| **data** | `/data` | 備份，**主要是放更新用的資料** | ❌ 明文 |

**只有 root 是加密的，這樣沒問題**，因為：

- boot 和 factory 裡的 kernel / rootfs 映像檔**本身就是加密的**
- `/data` 裡的更新檔案，敏感的部分我們自己要記得加密

`lsblk` 看到的樣子（rescue 方案）：

```
mmcblk2
|-mmcblk2p1        boot
|-mmcblk2p2        factory
|-mmcblk2p3        root
| `-root           ← dm-crypt 的虛擬裝置，掛在 / 上
`-mmcblk2p4        data
```

注意 `/` 掛的是 **`root` 這個虛擬裝置**，不是 `mmcblk2p3` 本身。
就是 §5 的 dm-crypt。

### `storage.info`：分割區的設計圖

`/factory/storage.info` 是純文字檔，factory-reset 時照它重建分割區：

```
boot:1:8M:+128M:ext4
factory:0:0:+500M:ext4
root:0:0:+4000M:ext4
data:0:0:0:ext4
```

每個欄位（用冒號分隔）：

| 欄位 | 意思 | `0` 代表 |
|---|---|---|
| 1 | 分割區名字 | （必填） |
| 2 | 分割區編號 | 交給系統決定 |
| 3 | 起始偏移 | 接在前一個分割區後面 |
| 4 | 大小 | 用到裝置結尾 |
| 5 | 檔案系統類型 | — |

### 💡 出廠時分割區會先「壓扁」

有個實務上的巧思：

**產線灌映像檔時，把分割區設成最小**，這樣要傳的資料變少、
初始化更快、**每片板子的生產時間變短**。

因為這階段所有資料都是靜態的，可以把要用的檔案全塞進 factory 分割區，
其他分割區留空。

**但有個限制**：改分割表容易（用 `sgdisk`），但要**不掉資料**地改，
就**不能移動有資料的分割區**。

在 rescue 方案裡，初始資料都在 factory 分割區，所以：
- `boot` 和 `factory` 是前兩個分割區，**必須一開始就給正確大小**（不能移動）
- `root` 和 `data` 可以先設成 **1MB**，factory-reset 時再撐開

```
出廠時的 fdisk -l：
/dev/loop9p1  ← boot，正確大小 128M
/dev/loop9p2  ← factory，正確大小 500M
/dev/loop9p3  ← root，只有 1M
/dev/loop9p4  ← data，只有 1M
```

---

### 方案一：Rescue（書頁 113–118｜PDF 131–136）

**核心想法**：留一個大的 factory 分割區，裡面放完整的出廠系統，
**隨時可以可靠地還原到出廠狀態**。

分割區：`boot` + `factory` + `root`（各一個）

`/boot/` 裡：
```
fitimage           ← kernel
rootfs.key.bb      ← 解 rootfs 的加密鑰匙（封起來的形式，caam-keygen 產的）
```

`/factory/` 裡：
```
fitimage           ← 出廠用的 kernel
rootfs             ← 出廠 rootfs（加密的）
rootfs.signature   ← 它的簽章
storage.info       ← 分割區設計圖
dek                ← 系統主加密鑰匙（廠商專屬）
```

> **`dek` 這個檔案**：i.MX8 上它是一個 wrapped 檔案。
> 但有些 CPU 用別的方式管理主鑰匙（例如放在受保護的 fuse 裡），
> **那些系統上根本不會有這個檔案**。

**開機時 U-Boot 印的**：
```
Running bootcmd [normal] on mmc2...
Schema: Rescue
```

**kernel command line**：
```
root=/dev/mmcblk2p3 ... initramfs_normal boot_schema=rescue root_name=root
                        ^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^
                        做一般開機         用 rescue 方案       root 分割區叫 root
```

**U-Boot 的初始變數**（書上用簡化過的 metacode 表達）：
```
schema=rescue
bootname=boot
rootname=root
image=fitimage
bootmode=normal
```

rescue 方案做 normal boot 時，**跟預設值沒什麼不同**——什麼都不用改。

**⚠️ 缺點**：要更新系統，必須**重開機 → 等更新跑完 → 才能跑新版**。
這些全在同一次開機序列裡完成，**安裝階段可能要好幾分鐘**
（看 rootfs 多大、CPU 多快）。這段時間系統是停的。

---

### 方案二：A/B（書頁 161–165｜PDF 179–183）

**核心想法**：**兩個 root 分割區輪流用**，
所以可以**在系統跑著的時候更新另一邊**。

**這是為了「系統不能停，連更新時都不能停」的場合。**

分割區：`boot` + `factory` + `root_a` + `root_b`

`lsblk` 看到的：
```
mmcblk2
|-mmcblk2p1        boot      256M（要放兩個 fitimage，所以加倍）
|-mmcblk2p2        factory   8M  （只有 8M！）
|-mmcblk2p3        root_a
|-mmcblk2p4        root_b
| `-root           ← 目前用的那一邊
`-mmcblk2p5        data
```

`/boot/` 裡：
```
fitimage_a
fitimage_b         ← 兩份 kernel
rootfs.key.bb      ← 一把鑰匙同時解 root_a 和 root_b
```

> 📌 上面是**已經更新過至少一次**的系統。出廠重置後第一次開機時，
> **`fitimage_a` 還不存在**。

`/factory/` 裡：
```
dek
storage.info
```
**出廠用的 fitimage 和它的憑證都不見了**——這就是為什麼 factory 分割區
可以縮到 8MB。

`storage.info`：
```
boot:1:8M:+256M:ext4
factory:0:0:+8M:ext4
root_a:0:0:+4000M:ext4
root_b:0:0:+4000M:ext4
data:0:0:0:ext4
```

**出廠時的分割區安排**（跟 rescue 不一樣）：
- 出廠 rootfs 壓縮檔放在 **`root_a`** 裡（不是 factory）
- factory-reset 時，系統裝進 **`root_b`**
- `root_a` 要等**第一次系統更新**時才被填滿

所以出廠時：`boot`（256M）、`factory`（8M）、`root_a`（夠大，裝出廠 rootfs）
是正確大小，`root_b` 和 `data` 各 1MB。

> ⚠️ **`root_a` 只能被放大，不能被移動**，否則裡面的資料會在裝新系統之前就沒了。

**開機時 U-Boot 印的**：
```
Running bootcmd [normal] on mmc2...
Schema: A/B [selector=b]
                     ^^^ 這次要跑 b 邊
```

**kernel command line**：
```
root=/dev/mmcblk2p4 ... initramfs_normal boot_schema=a_b root_name=root_b
```

**U-Boot 變數怎麼變的**：
```
初始：                     normal boot 時重新定義：
schema=a_b                schema=a_b
ab_selector=b             ab_selector=b
bootname=boot             bootname=boot
rootname=root      →      rootname=root_b     ← 加上 selector
image=fitimage     →      image=fitimage_b    ← 加上 selector
bootmode=normal           bootmode=normal
```

所以 `rootpart` 從 3 變成 4，載入的 kernel 從 `fitimage` 變成 `fitimage_b`。
**A/B 的全部魔法就是這個字尾。**

---

### 兩者比較

| | **Rescue** | **A/B** |
|---|---|---|
| root 分割區 | 1 個 | **2 個** |
| factory 分割區 | **大**（500MB，放完整出廠系統） | 小（8MB） |
| boot 分割區 | 128MB（1 個 fitimage） | 256MB（2 個 fitimage） |
| 總空間需求 | 較省 | **rootfs 空間加倍** |
| 更新時 | **必須重開機，停機好幾分鐘** | **邊跑邊更新，不停機** |
| 適合 | 空間吃緊、可以接受停機 | 不能停的系統 |

書上說：因為 A/B 要雙倍 rootfs 空間，**用 A/B 的系統通常會配比較大的儲存裝置**。

> 📄 **原文**　書 p.113 ｜ PDF p.131
>
> In the above list, the only encrypted partition is /root while other
> partitions are in plain text format. This is not a problem at all because in the
> boot and factory partitions all kernel and rootfs images are encrypted, while in
> /data we should be careful to encrypt all sensible files among the update
> binaries. [...] The factory schema is a way to boot the system, where we need a
> reliable way to restore the factory conditions.

<!-- -->
> 📄 **原文**　書 p.161 ｜ PDF p.179
>
> The A/B schema is a way to boot the system from two partitions
> alternatively. In this manner, we can update the system while it is running. In
> fact, as already seen, in the rescue schema, to update the system, we have to
> reboot it, then wait until the end of the update, and in the end, we can launch
> the new release. [...] the installation stage can take many minutes to complete,
> according to the rootfs size and the CPU speed.

📖 **書頁 109–118、161–165** ｜ PDF 頁 127–136、179–183 ｜ [開啟 PDF](./linux-secure-boot.pdf#page=127)

---

## §14 名詞小抄

| 名詞 | 全名 | 白話 |
|---|---|---|
| **ROM code** | — | 燒死在晶片裡、改不了的開機程式。信任鏈的第一棒，唯一無條件安全的東西 |
| **Root-of-Trust** | — | 信任的根。沒人驗它，靠物理/邏輯保護。通常就是 ROM code |
| **fuse** | — | 晶片裡一次性燒錄的儲存區。鑰匙燒進去就改不了 |
| **SPL** | Secondary Program Loader | U-Boot 的前導程式。主要任務：**把 DRAM 初始化**，讓大程式能跑 |
| **U-Boot** | Universal Bootloader | 嵌入式界的 GRUB。載入 kernel、傳參數 |
| **TF-A / ATF** | Trusted Firmware-A | ARM 的高權限韌體，扮演 secure monitor，負責載入 U-Boot 和 OP-TEE |
| **OP-TEE** | Open Portable Trusted Execution Environment | 跑在 Secure World 的迷你 OS，提供加密服務 |
| **TrustZone** | — | ARM 的硬體技術，把一顆 CPU 切成 Secure World 和 Normal World |
| **TEE / REE** | Trusted / Rich Execution Environment | TEE = 安全的小環境（OP-TEE）；REE = 一般的大環境（Linux） |
| **TA** | Trusted Application | 跑在 Secure World 裡的程式 |
| **CAAM** | Cryptographic Acceleration and Assurance Module | NXP i.MX 上的加密硬體：加密、雜湊、安全記憶體控制器、硬體亂數 |
| **DCP** | Data Co-Processor | 部分 i.MX 的加密加速器，**沒有自己的亂數源** |
| **TPM** | Trusted Platform Module | 專用安全晶片，安全存放鑰匙 |
| **HAB** | High Assurance Boot | NXP 的安全開機機制（書上出現在開機訊息裡，沒展開解釋） |
| **fitimage** | Flattened Image Tree | 一個檔案包住 kernel + Device Tree + initramfs |
| **DTB** | Device Tree Blob | 描述硬體長什麼樣的資料檔 |
| **initramfs** | initial RAM filesystem | 記憶體裡的迷你 root filesystem，任務是幫真 rootfs 起床（例如先解密） |
| **rootfs** | root filesystem | 那個 `/` |
| **switch_root** | — | 從 initramfs 切到真 rootfs。會**遞迴刪掉舊的 root** |
| **dm-crypt** | device-mapper crypt | 區塊層透明加密。做出 `/dev/mapper/root` |
| **fscrypt** | — | 檔案系統層加密（EXT4/F2FS/UBIFS 原生支援），可以只加密某些目錄 |
| **AF_ALG** | — | 讓使用者空間直接用 kernel 加密層的 socket 介面 |
| **keyring** | — | kernel 裡放鑰匙的「資料夾」。`@s` = session，`@u` = user |
| **seal / wrap** | 封 / 包 | 把鑰匙加密成一坨 blob，只有封它的東西能解開 |
| **KMK** | Kernel Master Key | 用來封 encrypted key 的那把 trusted key |
| **DEK** | Data Encryption Key | 系統主加密鑰匙。i.MX8 上是 `/factory/dek`，其他 CPU 可能沒有 |
| **eMMC** | embedded MultiMediaCard | NAND flash + 控制器包成一顆，用起來像硬碟 |
| **RPMB** | Replay-Protected Memory Block | eMMC 裡另一塊安全儲存區（`/dev/mmcblk2rpmb`） |
| **SSP** | Software Secure Provisioning | 產線灌韌體 + 燒鑰匙的整套最佳實務 |
| **IMA** | Integrity Measurement Architecture | Linux 的完整性量測機制，可以補 rootfs 沒簽章的洞 |
| **AES-CBC** | — | 本書用的對稱加密。CBC = 每塊先跟前一塊密文 XOR |
| **ECDSA** | Elliptic Curve DSA | 本書用的簽章演算法，配 SHA-256 |
| **FUSE** | Filesystem in Userspace | 讓非 root 使用者在使用者空間實作檔案系統的介面 |

---

## §15 書上沒講的（缺口清單）

書本自己明說「不在範圍」的東西，之後想深入就從這裡找：

| 主題 | 書上怎麼說 | 為什麼你可能會想補 |
|---|---|---|
| **Linux IMA** | 「不在本書涵蓋範圍」（書頁 81｜PDF 100） | **rootfs 沒簽章這個洞的唯一解**。優先度最高 |
| **keyring 細節** | 「本書不詳細解釋 keyring 是什麼」（書頁 19｜PDF 39） | 看 kernel 的 `Documentation/security/keys/` |
| **RPMB 的用法** | 「不在本書範圍」，給了 OP-TEE 文件連結（書頁 111｜PDF 129） | 另一個放鑰匙的安全地方 |
| **代工廠的 signed-bootloader 前置方案** | 「不在本書範圍」（書頁 100｜PDF 119） | 如果你的 CPU 不支援 ROM code 憑證，這是備案 |
| **kernel 內部怎麼用 crypto API** | 「本書不報告」（書頁 9｜PDF 29） | 只有寫 kernel driver 才需要 |
| **eCryptfs + encrypted key 的深入用法** | 指向 `Documentation/security/keys/ecryptfs.rst`（書頁 39｜PDF 59） | eCryptfs 已停止維護，優先度低 |
| **`dmsetup` 的其他選用參數** | 「超出本書範圍」，看 `man 8 dmsetup`（書頁 66｜PDF 86） | 調校時會用到 |
| **非 ARM 平台** | 全書以 ARM（i.MX、STM32MP1）為準 | x86 embedded 要另外查 |
| **Windows / macOS** | 「本書不涵蓋」（前言） | — |

### 這輪筆記自己跳過的（不是書上沒有，是我們決定不做）

- 第 3 章的**逐步操作**：Rescue 和 A/B 各自怎麼做 normal boot /
  factory-reset / system-update（書頁 118–189｜PDF 136–207）
- 第 4 章：產線怎麼產鑰匙（fuse-centric vs hybrid）、授權問題（書頁 191–204｜PDF 208–221）
- 附錄 A：防拆偵測（tamper detection）（書頁 205–｜PDF 222–）
- 附錄 B：U-Boot 環境變數是明文，怎麼保護跨階段的祕密（書頁 217–｜PDF 233–）

> 附錄 B 特別值得補——它處理的是 §9 提到的 kernel command line 明文問題。

---

## 一句話總結

> **Secure Boot = 一棒接一棒的驗簽 + 解密，
> 從燒死在晶片裡的 ROM code 開始，到掛載加密的 rootfs 為止。
> 掛載完成的那一刻，它就下班了。**
