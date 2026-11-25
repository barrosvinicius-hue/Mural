// ===== Funções usadas por TODAS as páginas =====

const API = "/api";

// Erro devolvido pelo servidor Flask: { erros: ["mensagem", ...] }
class ErroApi extends Error {
  constructor(erros, status) {
    super(erros.join(" "));
    this.erros = erros;
    this.status = status;
  }
}

async function requisicao(caminho, opcoes = {}) {
  let resposta;
  try {
    resposta = await fetch(API + caminho, opcoes);
  } catch (e) {
    throw new ErroApi(["Não foi possível falar com o servidor. O Flask está rodando?"], 0);
  }
  if (resposta.status === 204) return null;

  let dados = null;
  try { dados = await resposta.json(); } catch (e) { /* resposta sem JSON */ }

  if (!resposta.ok) {
    throw new ErroApi((dados && dados.erros) || ["Algo deu errado. Tente de novo."], resposta.status);
  }
  return dados;
}

// Atalhos para as rotas Flask
const api = {
  obter: (caminho) => requisicao(caminho),
  acao: (caminho) => requisicao(caminho, { method: "POST" }),
  remover: (caminho) => requisicao(caminho, { method: "DELETE" }),
  enviarJson: (metodo, caminho, dados) =>
    requisicao(caminho, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    }),
  enviarForm: (metodo, caminho, formData) => requisicao(caminho, { method: metodo, body: formData }),
};

// Cria um elemento HTML. Textos entram como texto (nunca como HTML), o que evita XSS.
function el(tag, atributos = {}, filhos = []) {
  const no = document.createElement(tag);
  for (const [nome, valor] of Object.entries(atributos)) {
    if (valor === false || valor === null || valor === undefined) continue;
    if (nome === "class") no.className = valor;
    else no.setAttribute(nome, valor === true ? "" : valor);
  }
  for (const filho of [].concat(filhos)) no.append(filho);
  return no;
}

// ----- avisos (substituem as mensagens "flash") -----
function mostrarAvisos(mensagens, tipo = "erro") {
  const area = document.getElementById("avisos");
  if (!area) return;
  area.replaceChildren(...[].concat(mensagens).map((texto) => el("p", { class: `aviso aviso-${tipo}` }, texto)));
}

function mostrarErro(erro) {
  mostrarAvisos(erro.erros || ["Algo deu errado. Tente de novo."]);
}

// Guarda um aviso para aparecer na PRÓXIMA página (depois de um redirecionamento)
function guardarAviso(texto) {
  try { sessionStorage.setItem("aviso", texto); } catch (e) { /* sem sessionStorage */ }
}

function mostrarAvisoGuardado() {
  try {
    const texto = sessionStorage.getItem("aviso");
    if (texto) {
      sessionStorage.removeItem("aviso");
      mostrarAvisos(texto, "ok");
    }
  } catch (e) { /* sem sessionStorage */ }
}

// ----- utilidades -----
function formatarData(texto) {            // "2026-11-25 14:30:00" -> "25/11/2026"
  const [ano, mes, dia] = String(texto).slice(0, 10).split("-");
  return `${dia}/${mes}/${ano}`;
}

function lerIdDaUrl() {                   // pages/wallpaper.html?id=3 -> 3
  const id = Number(new URLSearchParams(location.search).get("id"));
  return Number.isInteger(id) && id > 0 ? id : null;
}

mostrarAvisoGuardado();
