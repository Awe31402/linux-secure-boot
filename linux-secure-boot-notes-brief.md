# 讀書筆記 Brief — Secure Boot Encryption with Linux

- **書**：Rodolfo Giometti, *Secure Boot Encryption with Linux: Implementation for Embedded Developers* (Apress, 2026), 252 頁
- **檔案**：`/home/awe/security-and-crytography/linux-secure-boot.pdf`
- **定案日期**：2026-08-28
- **階段**：已收斂（framing → 完成），下一步產出大綱

---

## 1. Purpose

給自己的入門地圖。目標是讀完之後，能用自己的話講出「Linux 上的 secure boot
從開機到進系統，每一棒是誰、傳什麼、憑什麼相信下一棒」。

不是操作手冊，現階段不會照著做。它是之後回頭讀第 3、4 章時看得懂的底子。
因此筆記偏重**為什麼**，不是把指令抄下來。

## 2. Situation

- 這本書講的是**嵌入式 ARM 板子**的 secure boot：U-Boot、Yocto、i.MX8 / i.MX9、
  STM32MP1、CAAM 加密硬體、燒 fuse。
- **不是**一般 PC 那套 UEFI + shim + 微軟簽章。網路上搜「Linux secure boot」
  大部分是後者，兩者觀念相通但零件完全不同 —— 筆記要講清楚這個差別，
  避免日後查資料混淆。
- 作者假設讀者是資深嵌入式開發者，讀者本人不是。書裡當常識跳過的名詞
  （U-Boot SPL、fuse、CAAM 等）筆記要補一句白話解釋。

## 3. Inputs

- **主要來源**：`/home/awe/security-and-crytography/linux-secure-boot.pdf`，僅此一本。
- **範圍（骨幹版）**：
  - 第 1 章 Linux Cryptography — 書頁 p.1–75
  - 第 2 章 What Secure Boot Is (and What It Is NOT) — 書頁 p.77–107
  - 第 3 章 概念部分 — 書頁 p.109–118（Rescue schema 是什麼）、
    p.161–165（A/B schema 是什麼），不含逐步操作
- **不使用**：不上網查、不引用其他書或部落格。筆記要能對回書上頁碼。
- **缺口處理**：書上沒寫清楚的地方，明寫「書上沒講」，
  **不得自行補一個聽起來合理的答案**。要能分辨哪些是書上說的、哪些是缺口。

## 4. Limits

- 不要變成操作手冊。指令、程式碼只在「不看就講不清楚概念」時放，
  且僅放最小片段，不整段貼。
- 不延伸到骨幹以外：第 3 章逐步操作、第 4 章、附錄 A/B，這輪一律不碰。
- 不做技術選型建議（例如「你應該用 A/B 方案」）。現階段只要搞懂它們是什麼。
- 不為完整而完整。第 1 章的 API 細節若對理解主線無幫助就跳過，
  不必每節都交代。

## 5. Done-when

- **成品**：`/home/awe/security-and-crytography/linux-secure-boot-notes.md`
- **每節模板**：這在解決什麼問題 → 怎麼運作（白話）→ 名詞小抄 → 書上頁碼
- **份量**：約 8–12 頁 A4
- **完成標準**：不看書即可把開機信任鏈從第一棒講到掛載 root filesystem
- **第一個檢查點**：先交**大綱**（每節標題 + 2–3 句說明本節會講什麼），
  確認後才寫全文
- **選配**：全文完成後，可另外發一份瀏覽器可看的網頁版

---

## 已排除的選項（避免重複討論）

- 操作導向筆記（手上有板子、照著做）— 否決，現階段先求理解
- 全書涵蓋（含 Ch3 細節、Ch4、兩附錄）— 否決，先打底，之後想要再補
