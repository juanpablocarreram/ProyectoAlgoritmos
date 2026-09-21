const selectStat = document.getElementById("select-stat");
const selectAlgoritmo = document.getElementById("select-algoritmo");
const sliderPercentil = document.getElementById("slider-percentil");
const valorPercentil = document.getElementById("valor-percentil");
const resultadoPercentil = document.getElementById("resultado-percentil");
const resultadoUbicar = document.getElementById("resultado-ubicar");
const tarjetasContenedor = document.getElementById("tarjetas");
const infoPaso = document.getElementById("info-paso");

let ultimosJugadores = [];
let pasosPlanos = [];
let pasoActual = 0;

async function cargarStats() {
  const respuesta = await fetch("/api/stats");
  const datos = await respuesta.json();
  selectStat.innerHTML = "";
  for (const [clave, info] of Object.entries(datos)) {
    const opcion = document.createElement("option");
    opcion.value = clave;
    opcion.textContent = `${info.label} (${info.unidad})`;
    selectStat.appendChild(opcion);
  }
  ultimosJugadores = datos[selectStat.value]?.jugadores || [];
}

function aplanarRondas(rondas) {
  const plano = [];
  rondas.forEach((ronda, indiceRonda) => {
    ronda.pasos.forEach((paso) => {
      plano.push({ ...paso, ronda: indiceRonda, low: ronda.low, high: ronda.high, pivote: ronda.pivote });
    });
  });
  return plano;
}

function dibujarPaso() {
  tarjetasContenedor.innerHTML = "";
  if (pasosPlanos.length === 0) {
    infoPaso.textContent = "";
    return;
  }
  const paso = pasosPlanos[pasoActual];
  ultimosJugadores.forEach((jugador, indice) => {
    const tarjeta = document.createElement("div");
    tarjeta.className = "tarjeta";
    tarjeta.textContent = `${jugador.jugador}: ${jugador.valor}`;
    if (indice === paso.j) tarjeta.classList.add("puntero-j");
    if (indice === paso.i) tarjeta.classList.add("puntero-i");
    if (jugador.valor === paso.pivote) tarjeta.classList.add("pivote");
    tarjetasContenedor.appendChild(tarjeta);
  });
  infoPaso.textContent = `Ronda ${paso.ronda + 1} — j=${paso.j}, i=${paso.i}, pivote=${paso.pivote}, swap=${paso.swap}`;
}

document.getElementById("boton-siguiente").addEventListener("click", () => {
  if (pasoActual < pasosPlanos.length - 1) {
    pasoActual += 1;
    dibujarPaso();
  }
});

document.getElementById("boton-anterior").addEventListener("click", () => {
  if (pasoActual > 0) {
    pasoActual -= 1;
    dibujarPaso();
  }
});

function marcarPresetActivo() {
  document.querySelectorAll(".presets button").forEach((boton) => {
    boton.classList.toggle("activo", boton.dataset.percentil === sliderPercentil.value);
  });
}

sliderPercentil.addEventListener("input", () => {
  valorPercentil.textContent = sliderPercentil.value;
  marcarPresetActivo();
});

document.querySelectorAll(".presets button").forEach((boton) => {
  boton.addEventListener("click", () => {
    sliderPercentil.value = boton.dataset.percentil;
    valorPercentil.textContent = boton.dataset.percentil;
    marcarPresetActivo();
  });
});

selectStat.addEventListener("change", async () => {
  const respuesta = await fetch("/api/stats");
  const datos = await respuesta.json();
  ultimosJugadores = datos[selectStat.value].jugadores;
});

document.getElementById("boton-calcular").addEventListener("click", async () => {
  const cuerpo = {
    stat: selectStat.value,
    percentil: Number(sliderPercentil.value),
    algoritmo: selectAlgoritmo.value,
  };
  const respuesta = await fetch("/api/percentil", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cuerpo),
  });
  const datos = await respuesta.json();
  resultadoPercentil.textContent = `Corte: ${datos.valor_corte} (${datos.jugador ?? "sin jugador exacto"})`;
  pasosPlanos = aplanarRondas(datos.rondas);
  pasoActual = 0;
  dibujarPaso();
});

document.getElementById("boton-ubicar").addEventListener("click", async () => {
  const valor = Number(document.getElementById("input-valor-propio").value);
  const cuerpo = { stat: selectStat.value, valor };
  const respuesta = await fetch("/api/ubicar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cuerpo),
  });
  const datos = await respuesta.json();
  resultadoUbicar.textContent = `Quedarías en el percentil ${datos.percentil_estimado} de ${datos.total_jugadores} jugadores.`;
  pasosPlanos = aplanarRondas(datos.rondas);
  pasoActual = 0;
  dibujarPaso();
});

cargarStats();
