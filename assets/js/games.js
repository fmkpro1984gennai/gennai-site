/* GENNAI AI — ストアリンクの設定ファイル
 *
 * ここに URL を入れると自動でリンクになる。
 * 空欄（null）のままだと「近日公開」の押せないボタンとして表示される。
 *
 *   Google Play  →  https://play.google.com/store/apps/details?id=<パッケージ名>
 *   App Store    →  https://apps.apple.com/jp/app/id<数字>
 *
 * ios / android の null を、上の形の URL 文字列に書き換えるだけでよい。
 * slug は index.html のカードの data-slug と対応している。ここを書き換えるだけで
 * HTML には触らなくてよい。URL を入れたらブラウザで再読み込みして表示を確認する。
 */

window.GENNAI_GAMES = [
  { slug: "ponpon-tile",            title: "ぽんぽんタイル",       ios: "https://apps.apple.com/jp/app/id6807742726", android: null },
  { slug: "mizumichi-tsunagi",      title: "みずみちつなぎ",       ios: null, android: null },
  { slug: "nakamahazure-jump",      title: "なかまはずれジャンプ", ios: null, android: null },
  { slug: "yajirushi-daidasshutsu", title: "矢印大脱出",           ios: null, android: null },
  { slug: "quiz-tobiishi",          title: "クイズ飛び石",         ios: null, android: null },
  { slug: "irowake-labo",           title: "色分け実験室",         ios: null, android: null },
  { slug: "balance-koujou",         title: "バランス工場",         ios: null, android: null },
  { slug: "gattai-danball",         title: "合体段ボール",         ios: null, android: null }
];

/* ---- ここから下は書き換え不要 ----
 * HTML には最初から「近日公開」の無効ボタンが書いてある。
 * 上の表に URL が入っているものだけを、押せるリンクに差し替える。
 */
(function () {
  var games = window.GENNAI_GAMES || [];
  var LABEL = { ios: "App Store", android: "Google Play" };

  function activate(el, url, store) {
    var link = document.createElement("a");
    link.className = el.className;
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = LABEL[store];
    link.setAttribute("data-store", store);
    el.parentNode.replaceChild(link, el);
  }

  function apply() {
    for (var i = 0; i < games.length; i++) {
      var g = games[i];
      var card = document.querySelector('[data-slug="' + g.slug + '"]');
      if (!card) continue;
      ["ios", "android"].forEach(function (store) {
        var url = g[store];
        if (typeof url !== "string" || url.length === 0) return;
        var btn = card.querySelector('[data-store="' + store + '"]');
        if (btn) activate(btn, url, store);
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply);
  } else {
    apply();
  }
})();
