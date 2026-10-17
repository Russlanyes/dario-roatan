// Mobile nav toggle + contact form -> WhatsApp. Content works without this script.
(function () {
  var nav = document.getElementById("nav");
  var btn = nav && nav.querySelector(".nav-toggle");
  var menu = document.getElementById("nav-menu");
  if (btn && menu) {
    var setOpen = function (open) {
      nav.classList.toggle("nav-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    };
    btn.addEventListener("click", function () { setOpen(btn.getAttribute("aria-expanded") !== "true"); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { setOpen(false); btn.focus(); }
    });
  }

  // Shared contact form: no backend. Builds a WhatsApp message and opens the number
  // of the service line the visitor picked (lawn or pest).
  var form = document.querySelector(".quote-form");
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var es = form.getAttribute("data-lang") === "es";
    var val = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; };
    var line = val("f-line");
    var sel = document.getElementById("f-line");
    var lineLabel = sel ? sel.options[sel.selectedIndex].text : "";
    var number = line === "pest" ? form.getAttribute("data-pest") : form.getAttribute("data-lawn");
    var parts = [];
    var name = val("f-name"), area = val("f-area"), msg = val("f-msg");
    parts.push(es ? "Hola Darío" + (name ? ", soy " + name : "") + "." : "Hi Darío" + (name ? ", this is " + name : "") + ".");
    if (lineLabel) parts.push((es ? "Servicio: " : "Service: ") + lineLabel + ".");
    if (area) parts.push((es ? "Zona en Roatán: " : "Area in Roatán: ") + area + ".");
    if (msg) parts.push(msg);
    var url = "https://wa.me/" + number + "?text=" + encodeURIComponent(parts.join("\n"));
    window.open(url, "_blank", "noopener");
  });
})();
