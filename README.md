# GENNAI AI 公式サイト

GENNAI AI（提供者 Sherpal, LLC）が配信するスマートフォン向けカジュアルパズル 8 本の公式ホームページ。
依存ゼロの静的 HTML で、ビルド作業なしにフォルダごと置けば動く。日本語のみ（配信は日本国内）。

## 構成

```
index.html                トップ（ヒーロー／ゲーム一覧／会社情報／お問い合わせ／フッター）
privacy.html              プライバシーポリシー
assets/css/site.css       全ページ共通のスタイル（色・字体のトークンはここの :root）
assets/js/games.js        ストア URL の設定（後述）
assets/img/icons/         各ゲームのアイコン（256px と 128px）
assets/img/feature/       各ゲームのフィーチャーグラフィック（1024x500 JPEG）
assets/img/shots/         ぽんぽんタイルのストアスクショ（540x960 JPEG・4 枚）
tools/prepare_images.py   原本フォルダからサイト用の画像を作り直すスクリプト
tools/build_preview.py    見た目確認用の単一ファイル HTML を dist/ に書き出すスクリプト
dist/                     上のスクリプトの出力（確認用・公開対象ではない）
```

外部依存は Google Fonts（Zen Maru Gothic / Noto Sans JP）だけ。JS ライブラリは使っていない。

## ストア URL の入れ方

App Store と Google Play の URL は `assets/js/games.js` の `window.GENNAI_GAMES` 1 か所にまとまっている。
`ios` と `android` に URL の文字列を入れると、そのゲームのボタンが自動でリンクに変わる。
`null` のままなら「近日公開」の押せないボタンとして表示される。HTML 側は触らなくてよい。

- Google Play → `https://play.google.com/store/apps/details?id=<パッケージ名>`
- App Store → `https://apps.apple.com/jp/app/id<数字>`

JavaScript が無効な環境では、HTML に静的に書いてある「近日公開」ボタンがそのまま表示される。

## 画像の原本

サイトに置いてある画像は、すべて下記から縮小して作った複製。原本には手を加えていない。

- アイコン → `Work/OUTBOX/<slug>-icon/final/icon_1024_appstore.png`
  （ぽんぽんタイルのみ `Work/OUTBOX/ponpon-tile-icon/ponpon-tile_icon_1024_appstore.png`）
- フィーチャーグラフィック → `Work/OUTBOX/<slug>-store/googleplay/feature_graphic_1024x500.png`
- ぽんぽんタイルのスクショ → `Work/OUTBOX/ponpon-tile-store/googleplay/v2/export-final/gp/gp_1.png` 〜 `gp_4.png`

原本を差し替えたら `python tools/prepare_images.py` を実行すると `assets/img/` が作り直される。
他 7 本には実機スクショの最新版が無いため、カードはフィーチャーグラフィックだけで成立させている。

## プライバシーポリシーの原本

`privacy.html` の本文は `Work/OUTBOX/nanako-games-privacy/privacy-policy-ja.html` が SSOT。
このサイトの側は本文を一字も変えず取り込み、上下のヘッダーとフッターだけサイト共通のものに差し替えている
（見た目の統一のため、原本のインライン CSS は `assets/css/site.css` の `.doc` 以下の規則に置き換えてある）。

原本を更新したら、`<main>` の中身をこちらへ再コピーする。原本側だけ直してサイトを放置しない。

## 見た目の確認

`python tools/build_preview.py` を実行すると、CSS・JS・画像をすべて埋め込んだ単一ファイルが
`dist/preview-index.html` と `dist/preview-privacy.html` に書き出される。
このファイルは単体で開けるので、共有や確認に使える（ページ間のリンクは動かない）。

## デプロイ

どの静的ホスティングでも、このフォルダをそのまま置けば動く（サーバー側の処理は不要）。

- Cloudflare Pages → 新規プロジェクトで「Direct Upload」を選び、このフォルダを丸ごとアップロードする
- GitHub Pages → リポジトリに push し、Settings の Pages でブランチのルートを公開元に指定する
- Netlify → Netlify のサイト一覧にこのフォルダをドラッグ＆ドロップする

`dist/` は確認用なので公開に含めなくてよい。

## 掲載していないもの

以下は未実装または未検証のため、意図的に書いていない。実装・確認が済んでから足すこと。

- 「戻す機能」「オフライン対応」「課金なし」といった機能の訴求
- App Store / Google Play の URL（2026-09-08 時点でどのゲームも公開 URL が未確定）
