// ===== pages/categoria-form.html: cadastrar (sem ?id) ou editar (?id=3) =====

const id = lerIdDaUrl();
const formulario = document.getElementById("formulario");
const botaoSalvar = document.getElementById("salvar");
const campos = formulario.elements;

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  botaoSalvar.disabled = true;
  const dados = { nome: campos.nome.value, descricao: campos.descricao.value };
  try {
    await (id ? api.enviarJson("PUT", `/categorias/${id}`, dados) : api.enviarJson("POST", "/categorias", dados));
    guardarAviso("Categoria salva.");
    location.href = "categorias.html";
  } catch (erro) {
    mostrarErro(erro);
    botaoSalvar.disabled = false;
  }
});

(async function iniciar() {
  if (!id) return;
  const titulo = "Editar categoria";
  document.title = `${titulo} · Parede`;
  document.getElementById("titulo-pagina").textContent = titulo;
  botaoSalvar.textContent = "Salvar alterações";
  try {
    const c = await api.obter(`/categorias/${id}`);
    campos.nome.value = c.nome;
    campos.descricao.value = c.descricao;
  } catch (erro) {
    mostrarErro(erro);
    botaoSalvar.disabled = true;
  }
})();
