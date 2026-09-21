const selectStat = document.getElementById("select-stat");
const selectAlgoritmo = document.getElementById("select-algoritmo");
const sliderPercentil = document.getElementById("slider-percentil");
const valorPercentil = document.getElementById("valor-percentil");
const resultadoPercentil = document.getElementById("resultado-percentil");
const resultadoUbicar = document.getElementById("resultado-ubicar");
const tarjetasContenedor = document.getElementById("tarjetas");
const resumenPercentil = document.getElementById("resumen-percentil");
const leyenda = document.getElementById("leyenda");
const pistaPercentil = document.getElementById("pista-percentil");

let ultimosJugadores = [];
let corteActual = null;
let etiquetaActual = { bajo: "el valor más bajo", alto: "el valor más alto" };
let labelActual = "";

function actualizarPista() {
  const valor = sliderPercentil.value;
  const etiqueta = labelActual ? labelActual.charAt(0).toLowerCase() + labelActual.slice(1) : "esta estadística";
  pistaPercentil.textContent = `Selecciona ${valor} para ver a los jugadores que caen dentro del percentil ${valor}% de ${etiqueta}.`;
}

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
  const statInfo = datos[selectStat.value];
  ultimosJugadores = statInfo?.jugadores || [];
  etiquetaActual = { bajo: statInfo?.etiqueta_bajo, alto: statInfo?.etiqueta_alto };
  labelActual = statInfo?.label || "";
  actualizarPista();
  dibujarTarjetas();
}

function dibujarTarjetas() {
  tarjetasContenedor.innerHTML = "";
  ultimosJugadores.forEach((jugador) => {
    const tarjeta = document.createElement("div");
    tarjeta.className = "tarjeta";
    tarjeta.textContent = `${jugador.jugador}: ${jugador.valor}`;
    if (corteActual !== null) {
      tarjeta.classList.add(jugador.valor <= corteActual ? "dentro-percentil" : "fuera-percentil");
    }
    tarjetasContenedor.appendChild(tarjeta);
  });
}

function marcarPresetActivo() {
  document.querySelectorAll(".presets button").forEach((boton) => {
    boton.classList.toggle("activo", boton.dataset.percentil === sliderPercentil.value);
  });
}

sliderPercentil.addEventListener("input", () => {
  valorPercentil.textContent = sliderPercentil.value;
  marcarPresetActivo();
  actualizarPista();
});

document.querySelectorAll(".presets button").forEach((boton) => {
  boton.addEventListener("click", () => {
    sliderPercentil.value = boton.dataset.percentil;
    valorPercentil.textContent = boton.dataset.percentil;
    marcarPresetActivo();
    actualizarPista();
  });
});

selectStat.addEventListener("change", async () => {
  const respuesta = await fetch("/api/stats");
  const datos = await respuesta.json();
  const statInfo = datos[selectStat.value];
  ultimosJugadores = statInfo.jugadores;
  etiquetaActual = { bajo: statInfo.etiqueta_bajo, alto: statInfo.etiqueta_alto };
  labelActual = statInfo.label;
  corteActual = null;
  resultadoPercentil.textContent = "";
  resultadoUbicar.textContent = "";
  resumenPercentil.textContent = "";
  leyenda.hidden = true;
  actualizarPista();
  dibujarTarjetas();
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
  corteActual = datos.valor_corte;
  const dentro = ultimosJugadores.filter((j) => j.valor <= corteActual).length;
  const restante = 100 - cuerpo.percentil;
  resumenPercentil.textContent = `${dentro} de ${ultimosJugadores.length} jugadores (${cuerpo.percentil}%) tienen ${etiquetaActual.bajo} — el ${restante}% restante tiene ${etiquetaActual.alto}.`;
  leyenda.hidden = false;
  dibujarTarjetas();
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
  const restante = (100 - datos.percentil_estimado).toFixed(1);
  resultadoUbicar.textContent = `Estás dentro del ${datos.percentil_estimado}% de jugadores con ${etiquetaActual.bajo} (el ${restante}% restante tiene ${etiquetaActual.alto}).`;
  corteActual = valor;
  const dentro = ultimosJugadores.filter((j) => j.valor <= corteActual).length;
  resumenPercentil.textContent = `${dentro} de ${ultimosJugadores.length} jugadores tienen un valor menor o igual al tuyo (${corteActual}).`;
  leyenda.hidden = false;
  dibujarTarjetas();
});

cargarStats();
