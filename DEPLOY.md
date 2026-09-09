# 公開の手順（GitHub Pages ＋ gennai.ai）

## 今の状態
- ソース → GitHub `fmkpro1984gennai/gennai-site`（公開リポジトリ・main ブランチ直下をそのまま配信）
- 配信 → GitHub Pages。`https://fmkpro1984gennai.github.io/gennai-site/`
- 更新 → このフォルダを直して `git push` するだけ（1〜2 分で反映）。ビルド工程は無い

## gennai.ai で開けるようにする（GoDaddy の DNS 画面で 1 回だけ）

GoDaddy → マイプロダクト → gennai.ai → DNS → 「DNS レコード」で、次のとおりにする。

### 1. 先に消す／止める
- 「転送（Forwarding）」が設定されていれば **オフ**（今の「準備中」ページの正体）
- 種類 A・名前 `@` の既存レコード（GoDaddy の駐車用 IP。例 15.197.148.33 / 3.33.130.190）を **削除**
- 種類 CNAME・名前 `www` の既存レコードがあれば **削除**

### 2. 足す（5 本）
| 種類 | 名前 | 値 | TTL |
|---|---|---|---|
| A | @ | 185.199.108.153 | 600 |
| A | @ | 185.199.109.153 | 600 |
| A | @ | 185.199.110.153 | 600 |
| A | @ | 185.199.111.153 | 600 |
| CNAME | www | fmkpro1984gennai.github.io | 600 |

値の出典 → GitHub Docs「Managing a custom domain for your GitHub Pages site」（docs.github.com/pages）。末尾のドットは GoDaddy 側では不要。

### 3. 足し終わったら
このセッション（または次の Claude セッション）に「DNS 入れた」と言うだけ。以下は自動でやる。
1. GitHub Pages の「Custom domain」に `gennai.ai` を設定（リポジトリに `CNAME` ファイルが 1 つ増える）
2. DNS 検証が通るのを待ち、「Enforce HTTPS」をオン（証明書の発行に最大 1 時間）
3. `https://gennai.ai/` と `https://www.gennai.ai/`（→ gennai.ai に転送）が 200 を返すことを実測

## ストア申請に使う URL（gennai.ai が通った後の最終形）
- プライバシーポリシー → `https://gennai.ai/privacy.html`
- サポート URL（App Store） → `https://gennai.ai/#contact`
- gennai.ai がまだなら暫定で `https://fmkpro1984gennai.github.io/gennai-site/privacy.html`（ログイン不要の公開ページなので Google Play の要件は満たす）

## 注意
- `dist/` は見た目確認用の生成物で git に入れていない（`.gitignore`）
- ストア URL は `assets/js/games.js` に入れて push すればボタンがリンクに変わる
