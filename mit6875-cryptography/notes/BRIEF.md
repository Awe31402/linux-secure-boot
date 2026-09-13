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
| lec02 計算安全 / negligible / PRG | L2 `7YfYYIvyYb8` | ❌ **字幕壞掉**（語音被誤判成西班牙文，英文軌是亂碼）。且主題是 One-Way Functions |
| lec02（PRG 定義、隨機性來源） | L6 `fdr6RKyjhEs` | ✅ 部分對應，字幕品質好 |
| lec03 前半 hybrid argument / NBU | L6 `fdr6RKyjhEs` 後半 | ✅ 對得很好 |
| lec03 後半 stateful→stateless / PRF | L7 `SmIQNWXkxeQ` 前半 | ✅ 對得很好，字幕品質差但可校正 |

**未驗證（推測，做之前要確認）：**

| 2018 影片 | 猜測對應的 Fall 2022 |
|---|---|
| L2 One-Way Functions | lec06 |
| L3 Number Theory | lec07–08 |
| L4–L5 Hardcore Bits | lec06–07（Goldreich–Levin） |
| L7 後半（GGM 樹） | lec04 |
| L8 Trapdoor Functions | lec10 |
| L9–L10 Public Key Encryption | lec08–10 |
| L11 Learning with Errors | lec19 |
| L12–L14 Zero Knowledge | lec14–15 |
| L15–L16 MACs, Digital Signatures | lec05, lec11–12 |
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
- **先驗字幕品質**：檔案大小是最快的指標。80 分鐘的課正常是 400–600KB；只有 40KB 就是壞的。
  也可以用 `yt-dlp --list-subs` 看有沒有 `xx-orig` 這種軌 —— 有的話代表原始語音被誤判了。
