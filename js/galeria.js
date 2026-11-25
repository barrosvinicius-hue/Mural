// ===== index.html: galeria com filtros =====

const formFiltros = document.getElementById("filtros");
const campos = formFiltros.elements;
const grade = document.getElementById("grade");
const vazio = document.getElementById("vazio");
const carregando = document.getElementById("carregando");
const listaChips = document.getElementById("chips");
const resumo = document.getElementById("resumo");

let tagAtiva = "";
let temporizador = null;

// ----- filtros <-> endereço da página (?categoria=2&tag=azul) -----
function lerFiltrosDaUrl() {
  const p = new URLSearchParams(location.search);
  campos.q.value = p.get("q") || "";
  campos.categoria.value = p.get("categoria") || "";
  campos.orientacao.value = p.get("orientacao") || "";
  campos.ordem.value = p.get("ordem") || "recentes";
  campos.favoritos.checked = p.get("favoritos") === "1";
  tagAtiva = (p.get("tag") || "").toLowerCase();
}

function montarParametros() {
  const p = new URLSearchParams();
  if (campos.q.value.trim()) p.set("q", campos.q.value.trim());
  if (campos.categoria.value) p.set("categoria", campos.categoria.value);
  if (campos.orientacao.value) p.set("orientacao", campos.orientacao.value);
  if (campos.ordem.value !== "recentes") p.set("ordem", campos.ordem.value);
  if (campos.favoritos.checked) p.set("favoritos", "1");
  if (tagAtiva) p.set("tag", tagAtiva);
  return p;
}

// ----- desenho da página -----
function desenharCartao(w) {
  const link = `pages/wallpaper.html?id=${w.id}`;

  const estrela = el("button", {
    type: "button",
    class: `estrela${w.favorito ? " ligada" : ""}`,
    "aria-label": w.favorito ? "Remover dos favoritos" : "Adicionar aos favoritos",
    "aria-pressed": w.favorito ? "true" : "false",
  }, "★");
  estrela.addEventListener("click", () => alternarFavorito(w.id));

  return el("li", { class: "cartao" }, [
    el("a", { class: "cartao-imagem", href: link }, [
      el("img", { src: w.url_imagem, alt: w.titulo, loading: "lazy" }),
    ]),
    estrela,
    el("div", { class: "cartao-texto" }, [
      el("h2", {}, [el("a", { href: link }, w.titulo)]),
      el("p", { class: "meta" }, w.categoria),
      el("p", { class: "meta meta-tecnica" }, [el("span", {}, w.resolucao), el("span", {}, w.orientacao)]),
    ]),
  ]);
}

function desenharChips(tags) {
  const chips = tags.map((t) => {
    const chip = el("button", { type: "button", class: `chip${t.nome === tagAtiva ? " chip-ativo" : ""}` },
      [t.nome + " ", el("small", {}, t.total)]);
    chip.addEventListener("click", () => {
      tagAtiva = tagAtiva === t.nome ? "" : t.nome;
      carregar();
    });
    return chip;
  });
  if (tagAtiva && !tags.some((t) => t.nome === tagAtiva)) {
    chips.unshift(el("span", { class: "chip chip-ativo" }, tagAtiva));
  }
  listaChips.replaceChildren(...chips);
}

async function carregar() {
  const parametros = montarParametros();
  const texto = parametros.toString();
  history.replaceState(null, "", texto ? `?${texto}` : location.pathname);

  carregando.hidden = false;
  try {
    const [lista, numeros] = await Promise.all([
      api.obter(`/wallpapers?${texto}`),
      api.obter("/resumo"),
    ]);
    resumo.textContent = `${numeros.total} wallpapers cadastrados, ${numeros.favoritos} favoritos.`;
    desenharChips(numeros.tags);
    grade.replaceChildren(...lista.wallpapers.map(desenharCartao));
    vazio.hidden = lista.wallpapers.length > 0;
  } catch (erro) {
    mostrarErro(erro);
  } finally {
    carregando.hidden = true;
  }
}

async function alternarFavorito(id) {
  try {
    await api.acao(`/wallpapers/${id}/favorito`);
    await carregar();
  } catch (erro) {
    mostrarErro(erro);
  }
}

// ----- eventos -----
formFiltros.addEventListener("submit", (e) => { e.preventDefault(); carregar(); });

for (const nome of ["categoria", "orientacao", "ordem", "favoritos"]) {
  campos[nome].addEventListener("change", carregar);
}

campos.q.addEventListener("input", () => {        // espera o usuário parar de digitar
  clearTimeout(temporizador);
  temporizador = setTimeout(carregar, 300);
});

document.getElementById("limpar").addEventListener("click", () => {
  formFiltros.reset();
  campos.ordem.value = "recentes";
  tagAtiva = "";
  carregar();
});

// ----- início -----
(async function iniciar() {
  try {
    const { categorias } = await api.obter("/categorias");
    for (const c of categorias) campos.categoria.append(el("option", { value: c.id }, c.nome));
    lerFiltrosDaUrl();
    await carregar();
  } catch (erro) {
    carregando.hidden = true;
    mostrarErro(erro);
  }
})();
