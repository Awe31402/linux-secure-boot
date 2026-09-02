# MIT 6.5620 / 6.875 / 18.425 — Foundations of Cryptography (Fall 2022)

Course materials mirrored from the official site.
Instructor: Vinod Vaikuntanathan (MIT).

- Course website: https://mit6875.github.io/fall2022.html
- **Lecture videos (YouTube playlist): https://www.youtube.com/playlist?list=PL6ogFv-ieghe8MOIcpD6UDtdK-UMHG8oH**

## Contents

```
slides/   lec01.pdf … lec25.pdf  (+ lec18.pptx)
psets/    hw1, hw3, hw4, hw5, hw6
```

## Known gaps

| Item | Status |
|---|---|
| `slides/lec18.pdf` | The PDF link on the course site returns 404. The `.pptx` was downloaded instead (`slides/lec18.pptx`). |
| `psets/hw2.pdf` | The link on the course site returns 404. Not available anywhere on the site. |

## Lecture index

| # | Topics |
|---|---|
| 1 | Intro to cryptography; Shannon perfect secrecy; one-time pad; Shannon's lower bound |
| 2 | Computational adversaries; computational security; pseudorandom generators (PRG); stateful secret-key encryption |
| 3 | The hybrid argument; PRG length extension; pseudorandom functions (PRF); PRFs ⇒ secret-key encryption |
| 4 | Formal PRF security; the GGM PRF construction; IND-CPA secure encryption |
| 5 | Identification protocols; message authentication codes (MAC); CCA-secure symmetric encryption |
| 6 | One-way functions; hardcore bits; the Goldreich–Levin theorem |
| 7 | Goldreich–Levin (contd.); local list decoding; primes and Z_p*; discrete log |
| 8 | Merkle key exchange; public-key encryption; IND-CPA; group & number theory overview |
| 9 | Discrete log assumption; Diffie–Hellman key exchange; El Gamal; factoring; RSA |
| 10 | Trapdoor functions; RSA trapdoor permutations; QRA; Goldwasser–Micali; digital signature motivation (EUF-CMA) |
| 11 | Digital signatures: definitions; Lamport one-time signatures |
| 12 | Collision-resistant hash functions; many-time stateful signatures; Naor–Yung |
| 13 | CRHF from discrete log; signatures from RSA; hash-and-sign; the random oracle heuristic |
| 14 | Zero knowledge I: definitions and examples |
| 15 | Zero knowledge II: ZK proofs for all of NP |
| 16 | Proofs of knowledge; Fiat–Shamir |
| 17 | Succinct (zero-knowledge) argument systems; Merkle trees; PCPs; Kilian's protocol |
| 18 | Lattice-based cryptography (intro) — *lecture cancelled; slides only* |
| 19 | Lattices and Learning With Errors (LWE); LWE-based encryption & hashing; fully homomorphic encryption (FHE) |
| 20 | FHE continued: bootstrapping, circular security; open problems |
| 21 | Oblivious transfer; private information retrieval |
| 22 | Secure two-party computation; the Goldreich–Micali–Wigderson protocol |
| 23 | Secret sharing; secure multiparty computation |
| 24 | Program obfuscation and applications |
| 25 | Yao's garbled circuits |

Lectures 26 (quantum cryptography) and 27 (grand challenges / AMA) have video only — no slides were posted.

## Suggested references

- Katz–Lindell, *Introduction to Modern Cryptography*
- Boneh–Shoup, *A Graduate Course in Applied Cryptography* — http://toc.cryptobook.us/book.pdf
- Goldreich, *Foundations of Cryptography*
- Pass–Shelat lecture notes — https://www.cs.cornell.edu/courses/cs4830/2010fa/lecnotes.pdf
