// ===== pages/categorias.html: lista de categorias =====

const corpo = document.getElementById("corpo");
const tabela = document.getElementById("tabela");
const vazio = document.getElementById("vazio");

function desenharLinha(c) {
  const excluir = el("button", {
    type: "button",
    class: "link-perigo",
    disabled: c.total_wallpapers > 0,
    title: c.total_wallpapers > 0 ? "Mova ou exclua os wallpapers desta categoria primeiro" : false,
  }, "Excluir");
  excluir.addEventListener("click", () => excluirCategoria(c));

  return el("tr", {}, [
    el("td", {}, [el("a", { href: `../index.html?categoria=${c.id}` }, c.nome)]),
    el("td", {}, c.descricao || "—"),
    el("td", { class: "num" }, c.total_wallpapers),
    el("td", { class: "acoes-tabela" }, [el("a", { href: `categoria-form.html?id=${c.id}` }, "Editar"), excluir]),
  ]);
}

async function carregar() {
  try {
    const { categorias } = await api.obter("/categorias");
    corpo.replaceChildren(...categorias.map(desenharLinha));
    tabela.hidden = categorias.length === 0;
    vazio.hidden = categorias.length > 0;
  } catch (erro) {
    mostrarErro(erro);
  }
}

async function excluirCategoria(c) {
  if (!window.confirm(`Excluir a categoria “${c.nome}”?`)) return;
  try {
    await api.remover(`/categorias/${c.id}`);
    mostrarAvisos("Categoria excluída.", "ok");
    await carregar();
  } catch (erro) {
    mostrarErro(erro);
  }
}

carregar();
