// ===== pages/wallpaper-form.html: cadastrar (sem ?id) ou editar (?id=3) =====

const id = lerIdDaUrl();
const formulario = document.getElementById("formulario");
const entradaImagem = document.getElementById("imagem");
const previa = document.getElementById("previa");
const previaVazia = document.getElementById("previa-vazia");
const botaoSalvar = document.getElementById("salvar");
const campos = formulario.elements;

function mostrarPrevia(endereco) {
  previa.src = endereco;
  previa.hidden = false;
  previaVazia.hidden = true;
}

entradaImagem.addEventListener("change", () => {
  const arquivo = entradaImagem.files[0];
  if (arquivo) mostrarPrevia(URL.createObjectURL(arquivo));
});

function modoEdicao(w) {
  const titulo = "Editar wallpaper";
  document.title = `${titulo} · Parede`;
  document.getElementById("titulo-pagina").textContent = titulo;
  botaoSalvar.textContent = "Salvar alterações";
  document.getElementById("dica-imagem").textContent = "Deixe em branco para manter a imagem atual. PNG, JPG ou WEBP, até 5 MB.";
  entradaImagem.required = false;
  document.getElementById("cancelar").href = `wallpaper.html?id=${w.id}`;

  campos.titulo.value = w.titulo;
  campos.categoria_id.value = w.categoria_id;
  campos.autor.value = w.autor;
  campos.tags.value = w.tags.join(", ");
  campos.descricao.value = w.descricao;
  mostrarPrevia(w.url_imagem);
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  botaoSalvar.disabled = true;
  try {
    const dados = new FormData(formulario);               // inclui o arquivo da imagem
    const w = id
      ? await api.enviarForm("PUT", `/wallpapers/${id}`, dados)
      : await api.enviarForm("POST", "/wallpapers", dados);
    guardarAviso(id ? "Alterações salvas." : "Wallpaper cadastrado.");
    location.href = `wallpaper.html?id=${w.id}`;
  } catch (erro) {
    mostrarErro(erro);
    window.scrollTo({ top: 0 });
    botaoSalvar.disabled = false;
  }
});

(async function iniciar() {
  try {
    const { categorias } = await api.obter("/categorias");
    for (const c of categorias) campos.categoria_id.append(el("option", { value: c.id }, c.nome));
    document.getElementById("sem-categoria").hidden = categorias.length > 0;

    if (id) modoEdicao(await api.obter(`/wallpapers/${id}`));
    else entradaImagem.required = true;
  } catch (erro) {
    mostrarErro(erro);
  }
})();
