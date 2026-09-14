# 課堂筆記 Brief（6.875 Fall 2022）

lec01 依此製作；確認可用後，之後每堂沿用同一份規格。

## 1. 目的 (Purpose)

自己複習用。回頭看筆記就能想起整堂課在講什麼，不必重看影片。

因此：重定義、重直覺、重「為什麼這樣設計」。行政事項、課程公告、閒聊一律刪掉。

## 2. 背景 (Situation)

- 自學 MIT 6.5620 / 6.875 / 18.425 — Foundations of Cryptography, Fall 2022，講者 Vinod Vaikuntanathan。
- lec01 主題：intro to cryptography、Shannon perfect secrecy、one-time pad、Shannon's lower bound。
- repo 原本沒有 `notes/`。lec01 這一份是模板，之後 26 堂照著做。
- 教材完整：25 份投影片、6 份 pset、Boneh–Shoup 教科書。

## 3. 材料 (Inputs)

主要來源，依權威性排序：

1. `slides/lec01.pdf` — 所有正式內容（定義、定理敘述、證明結構）以投影片為準。
2. YouTube 自動字幕 — 補直覺、口頭解釋、投影片上沒寫的「為什麼」。

**⚠️ 影片與投影片年份不同。** 線上唯一一套 6.875 錄影是 **2018 年春季**的學生上傳版
（頻道 Andrew Xia）。README 裡標為「Fall 2022 lecture videos」的播放清單其實就是這套。
MIT 沒有公開 Fall 2022 的錄影。

- lec01：兩邊內容一致（Shannon perfect secrecy → one-time pad → |K| ≥ |M|），可以互補。
  影片：https://youtu.be/jDsfV2ohFPs
- **lec02 起編號對不上**：播放清單 L2 = One-Way Functions、L3 = Number Theory，
  但 Fall 2022 的 lec02 = PRG、lec03 = hybrid argument / PRF。
  之後每堂都要先按主題比對，不能照編號抓。
- 行政事項（TA、評分、平台）兩邊完全不同 —— 一律以投影片為準，或直接刪掉。

規則：

- 自動字幕品質很差（會把 cryptography 一路聽成 "photography"），數學名詞一律用投影片校正。
- 兩邊都沒講清楚的地方，**可以**用自己的知識或 `books/` 的教科書補，但必須明確標記為外部補充，不可與課堂內容混淆。
- 補充維持少量，不喧賓奪主。

## 4. 界線 (Limits)

- 只新增 `notes/` 底下的檔案。不修改 `slides/`、`psets/`、`books/`、`README.md`。
- 一次只做一堂。
- 不往前引用之後的課（不寫「這個 lec03 會解決」這類伏筆）。
- 不自行 `git commit`。

## 5. 完成條件 (Done-when)

- 檔案：`notes/lecNN.md`
- 語言：繁體中文為主，技術術語保留英文原文（perfect secrecy、one-time pad、ciphertext…）。
- 格式：Markdown，數學用 `$...$` / `$$...$$`。
- 結構：
  1. 一句話總結
  2. 這堂要回答什麼問題
  3. 分節內容（定義 / 直覺 / 證明骨架）
  4. 名詞對照表
  5. 外部補充區（標記清楚）
  6. 存疑處（標 `⚠️` 與影片時間點）
- 檢查點：**先交大綱**（骨架 + 各節標題），確認方向後才寫滿。

---

## 附錄：影片對照表（working map）

2018 播放清單的編號**不能**直接對到 Fall 2022 的投影片。每做一堂之前，先按**主題**比對。

**已驗證：**

| Fall 2022 投影片 | 2018 影片 | 狀況 |
|---|---|---|
| lec01 Intro / perfect secrecy / OTP | L1 `jDsfV2ohFPs` | ✅ 內容一致，字幕差但可用 |
| lec02 計算安全 / negligible / 計算不可區分性 | L2 `7YfYYIvyYb8` 前半 | ✅ **YouTube 字幕壞掉，已自行用 Whisper 轉錄**，品質好。後半是 one-way functions（= lec06） |
| lec02（PRG 定義、隨機性來源） | L6 `fdr6RKyjhEs` | ✅ 部分對應，字幕品質好 |
| lec03 前半 hybrid argument / NBU | L6 `fdr6RKyjhEs` 後半 | ✅ 對得很好 |
| lec03 後半 stateful→stateless / PRF | L7 `SmIQNWXkxeQ` 前半 | ✅ 對得很好，字幕品質差但可校正 |
| lec04 PRF 安全性 / GGM / IND-CPA | L7 `SmIQNWXkxeQ` 後半（53:21 之後） | ✅ GGM 結構一致。⚠️ **lec04.pdf 是手寫講義，沒有文字層，要當圖讀** |
| lec05 MAC / EUF-CMA 部分 | L15 `Kp2JqEuoTuI` 前半 | △ 只涵蓋 MAC 那段 |
| lec05 challenge-response、學習理論、IND-CCA2 | — | ❌ **沒有影片**（L15、L16 都查過了） |
| lec06 OWF 定義 | L2 `7YfYYIvyYb8` `[43:40]`– | ✅ 自轉稿 |
| lec06 Hardcore bits | L4 `H008GInK0xc` `[43:40]`–`[48:16]` | ✅ **自轉**（YouTube 版漏掉近三成內容） |
| lec06 OWP ⇒ PRG | L6 `fdr6RKyjhEs` `[72:39]`– | ✅ YouTube 字幕即可 |
| lec06 Goldreich–Levin | L5 `UuQuF0tcn1E` | ✅ 自轉稿 |
| lec07 discrete log / MSB hardcore | L4 `H008GInK0xc` `[51:42]`– | ✅ 已有自轉稿，做 lec07 時直接用 |

**未驗證（推測，做之前要確認）：**

| 2018 影片 | 猜測對應的 Fall 2022 |
|---|---|
| L3 Number Theory | lec07–08 |
| L8 Trapdoor Functions | lec10 |
| L9–L10 Public Key Encryption | lec08–10 |
| L11 Learning with Errors | lec19 |
| L12–L14 Zero Knowledge | lec14–15 |
| L15 後半 + L16 簽章 / CRHF | lec11–13 |
| L17 Hash Functions, Random Oracles | lec12–13 |
| L19 Oblivious Transfer, 2PC | lec21–22 |
| L20 Garbled Circuits | lec25 |
| L21–L22 BGW MPC, Malicious | lec23 |
| L23–L24 FHE, PIR | lec19–21 |

Fall 2022 的 lec16（Fiat–Shamir）、lec17（succinct arguments）、lec18（lattices）、lec24（obfuscation）
在 2018 那套裡**沒有對應影片**。

## 附錄：操作筆記

- **投影片先試文字層**：`pdftotext -layout slides/lecNN.pdf out.txt`。lec02 有文字層，比讀圖快很多。
  但文字層會把動畫疊印的兩個版本混在一起、數學上下標也會壞 —— 公式一律回頭對照 PDF 的圖。
- **抓字幕**：`yt-dlp --no-update --skip-download --write-auto-subs --sub-langs en --sub-format vtt`
- **會被限流**：連續抓幾支會拿到 HTTP 429。等 45 秒重試，通常第 3 次會過。
- **有些投影片是手寫的**：`lec04.pdf` 沒有文字層，`pdftotext` 出來是 OCR 亂碼，要用 Read 的 `pages` 當圖讀。
  先跑 `pdftotext` 看一眼，輸出像亂碼就改讀圖。
- **符號會跨堂衝突**：lec03 和 lec05 用 $\ell$/$m$ = 輸入/輸出長度、$n$ = 安全參數；
  lec04 用 $m$/$n$ = 輸入/輸出、$\lambda$ = 安全參數。**lec04 是特例。**
  每堂開頭先確認該堂的符號慣例，並在筆記裡標出與前一堂的差異。
- **不是每堂都有影片**：lec05 有三段（challenge-response、學習理論、IND-CCA2）在 2018 那套裡完全沒有。
  投影片有文字層時這不太要緊；先確認投影片完整度，再決定要花多少力氣找影片。
- **先驗字幕品質**：檔案大小是最快的指標。80 分鐘的課正常是 400–600KB；只有 40KB 就是壞的。
  也可以用 `yt-dlp --list-subs` 看有沒有 `xx-orig` 這種軌 —— 有的話代表原始語音被誤判了。

## 附錄：自行轉錄逐字稿（字幕壞掉時）

YouTube 的自動字幕品質差異很大，有些（如 L2）根本是壞的。這時自己轉，品質好非常多
（有標點、有大小寫、術語錯誤少）。**lec02 就是這樣救回來的。**

環境已經備妥（`~/.local`，沒有動系統 Python）：

```bash
# 1. 下載音訊
yt-dlp --no-update -f bestaudio -x --audio-format mp3 --audio-quality 5 \
       -o "LNN_audio.%(ext)s" "https://youtu.be/<VIDEO_ID>"

# 2. 轉錄（RTX 4060 上 81 分鐘的課約 7 分鐘）
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
whisper LNN_audio.mp3 --model turbo --language en --device cuda \
  --output_dir whisper_out --output_format all --verbose False \
  --initial_prompt "MIT 6.875 Foundations of Cryptography, lecture by Vinod
  Vaikuntanathan. Topics: one-way functions, pseudorandom generators, negligible
  functions, security parameter, probabilistic polynomial time, adversary,
  distinguisher, hardcore bits, Goldreich-Levin, discrete logarithm, factoring,
  RSA, indistinguishability, reduction, XOR, ciphertext, plaintext."
```

然後用 `whisper_out/*.tsv`（欄位是 `start` / `end` / `text`，start 是毫秒）整理成帶時間點的段落。

**踩過的坑：**

- **不要用 `large-v3`。** 它載入時是 fp32（約 6GB+），8GB 的卡會 CUDA OOM。
  **`turbo`** 是 large-v3 的蒸餾版，快很多、品質接近，穩穩放得下。
- **`--initial_prompt` 很有效**，會大幅改善專有名詞。但 Whisper 仍會把 cryptography 聽成 "photography"。
  **數學內容一律以投影片為準。**
- **背景執行時不要把輸出接到 `tail`** —— `$?` 會抓到 `tail` 的結果，任務「成功」但其實爆了。
  改成 `> run.log 2>&1` 再看 log。
- 逐字稿留在 scratchpad，**不要 commit 進 repo**。
- **Whisper 對人名特別弱**：Goldreich–Levin → "Goldrack"、Chernoff → "Chernobyl"。
  數學名詞靠 `--initial_prompt` 救得回來，人名救不太回來 —— 一律用投影片校正。
- **一堂課的材料可能散在四支影片裡**（lec06 就是 L2 + L4 + L5 + L6）。
  先用 `grep -o -i` 統計關鍵術語出現次數，快速判斷哪支涵蓋哪一段，再去讀。

**先判斷值不值得轉：**

YouTube 有兩代自動字幕。**新版**（有標點、有大小寫）品質已經很好，自己轉**沒有加值**；
**舊版**（無標點、全小寫、術語大量錯誤）才值得自轉。

實測（L6，2018 年的 PRG 那堂，YouTube 是新版字幕）：

| 詞 | YouTube | 自轉 Whisper |
|---|---|---|
| pseudorandom | 64 | 18 |
| "subrandom"（錯的） | 0 | 6 |
| distinguisher | 38 | 34 |

**自轉版反而更差** —— 它把 pseudorandom generator 聽成 "subrandom generated"。字數與涵蓋範圍則幾乎相同。

所以流程是：**先看字幕有沒有標點。有就直接用；沒有（或整份是 `[Music]`）才自轉。**
