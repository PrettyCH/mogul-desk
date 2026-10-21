/**
 * Mogul Desk — lightweight compare-table + entry-card filter.
 * Expects a .filter-bar[data-compare-root] near table.compare / .entry cards.
 * Rows: tr[data-entry][data-<group>]  Entries: article.entry[data-entry][data-<group>]
 */
(function () {
  "use strict";

  function normalize(s) {
    return (s || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  function initRoot(root) {
    var search = root.querySelector("[data-filter-search]");
    var groups = Array.prototype.slice.call(
      root.querySelectorAll("[data-filter-group]")
    );
    var status = root.querySelector("[data-filter-status]");
    var countEl = root.querySelector("[data-filter-count]");

    var scope =
      root.closest("main") ||
      root.parentElement ||
      document;

    var rows = Array.prototype.slice.call(
      scope.querySelectorAll("table.compare tbody tr[data-entry]")
    );
    var entries = Array.prototype.slice.call(
      scope.querySelectorAll("article.entry[data-entry]")
    );

    var active = {};
    groups.forEach(function (g) {
      active[g.getAttribute("data-filter-group")] = "";
    });

    function selectedValue(groupEl) {
      var on = groupEl.querySelector(".filter-chip.is-active");
      return on ? on.getAttribute("data-filter-value") || "" : "";
    }

    function matchItem(el) {
      for (var i = 0; i < groups.length; i++) {
        var key = groups[i].getAttribute("data-filter-group");
        var want = active[key];
        if (!want) continue;
        var got = el.getAttribute("data-" + key) || "";
        if (got !== want) return false;
      }
      var q = normalize(search ? search.value : "");
      if (!q) return true;
      var hay =
        (el.getAttribute("data-search") || "") +
        " " +
        (el.textContent || "");
      return normalize(hay).indexOf(q) !== -1;
    }

    function apply() {
      groups.forEach(function (g) {
        active[g.getAttribute("data-filter-group")] = selectedValue(g);
      });

      var visibleIds = {};
      var shown = 0;
      var total = Math.max(rows.length, entries.length);

      rows.forEach(function (tr) {
        var ok = matchItem(tr);
        tr.hidden = !ok;
        tr.setAttribute("aria-hidden", ok ? "false" : "true");
        if (ok) {
          shown++;
          visibleIds[tr.getAttribute("data-entry")] = true;
        }
      });

      // If no rows (shouldn't happen), count from entries
      if (rows.length === 0) {
        shown = 0;
        entries.forEach(function (art) {
          if (matchItem(art)) {
            shown++;
            visibleIds[art.getAttribute("data-entry")] = true;
          }
        });
      } else {
        // Sync entry cards to row visibility by id; also re-check search on card
        entries.forEach(function (art) {
          var id = art.getAttribute("data-entry");
          var ok = !!visibleIds[id];
          // If row missing, fall back to matching the card itself
          if (!rows.some(function (r) {
            return r.getAttribute("data-entry") === id;
          })) {
            ok = matchItem(art);
          }
          art.hidden = !ok;
          art.setAttribute("aria-hidden", ok ? "false" : "true");
        });
      }

      if (status) {
        var empty = shown === 0;
        status.hidden = !empty;
        status.setAttribute("aria-hidden", empty ? "false" : "true");
      }
      if (countEl) {
        countEl.textContent =
          shown === total
            ? "共 " + total + " 条"
            : "显示 " + shown + " / " + total + " 条";
      }
    }

    groups.forEach(function (g) {
      g.addEventListener("click", function (e) {
        var btn = e.target.closest(".filter-chip");
        if (!btn || !g.contains(btn)) return;
        e.preventDefault();
        Array.prototype.forEach.call(
          g.querySelectorAll(".filter-chip"),
          function (b) {
            b.classList.remove("is-active");
            b.setAttribute("aria-pressed", "false");
          }
        );
        btn.classList.add("is-active");
        btn.setAttribute("aria-pressed", "true");
        apply();
      });
    });

    if (search) {
      search.addEventListener("input", apply);
      search.addEventListener("search", apply);
    }

    var clearBtn = root.querySelector("[data-filter-clear]");
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        if (search) search.value = "";
        groups.forEach(function (g) {
          Array.prototype.forEach.call(
            g.querySelectorAll(".filter-chip"),
            function (b, i) {
              var on = i === 0;
              b.classList.toggle("is-active", on);
              b.setAttribute("aria-pressed", on ? "true" : "false");
            }
          );
        });
        apply();
        if (search) search.focus();
      });
    }

    apply();
  }

  function boot() {
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-compare-root]"),
      initRoot
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
