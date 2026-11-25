// ===== pages/wallpaper.html: detalhe de um wallpaper =====

const id = lerIdDaUrl();
const detalhe = document.getElementById("detalhe");
const naoEncontrado = document.getElementById("nao-encontrado");
const botaoFavorito = document.getElementById("favoritar");

function desenhar(w) {
  document.title = `${w.titulo} · Parede`;
  const imagem = document.getElementById("imagem");
  imagem.src = w.url_imagem;
  imagem.alt = w.titulo;

  document.getElementById("titulo").textContent = w.titulo;
  const descricao = document.getElementById("descricao");
  descricao.textContent = w.descricao;
  descricao.hidden = !w.descricao;

  document.getElementById("categoria").textContent = w.categoria;
  document.getElementById("resolucao").textContent = `${w.resolucao} (${w.orientacao.toLowerCase()})`;
  document.getElementById("autor").textContent = w.autor || "Não informado";
  document.getElementById("data").textContent = formatarData(w.data_cadastro);

  const tags = document.getElementById("tags");
  tags.replaceChildren(...(w.tags.length
    ? w.tags.map((t) => el("a", { class: "chip", href: `../index.html?tag=${encodeURIComponent(t)}` }, t))
    : ["Sem tags"]));

  document.getElementById("editar").href = `wallpaper-form.html?id=${w.id}`;
  const baixar = document.getElementById("baixar");
  baixar.href = w.url_imagem;
  baixar.setAttribute("download", w.arquivo);
  botaoFavorito.textContent = w.favorito ? "Remover dos favoritos" : "Adicionar aos favoritos";

  detalhe.hidden = false;
}

botaoFavorito.addEventListener("click", async () => {
  try {
    desenhar(await api.acao(`/wallpapers/${id}/favorito`));
  } catch (erro) {
    mostrarErro(erro);
  }
});

document.getElementById("excluir").addEventListener("click", async () => {
  if (!window.confirm("Excluir este wallpaper? Esta ação não pode ser desfeita.")) return;
  try {
    await api.remover(`/wallpapers/${id}`);
    guardarAviso("Wallpaper excluído.");
    location.href = "../index.html";
  } catch (erro) {
    mostrarErro(erro);
  }
});

(async function iniciar() {
  if (!id) { naoEncontrado.hidden = false; return; }
  try {
    desenhar(await api.obter(`/wallpapers/${id}`));
  } catch (erro) {
    if (erro.status === 404) naoEncontrado.hidden = false;
    else mostrarErro(erro);
  }
})();
