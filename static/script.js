function enviarFormulario() {
  const form = document.getElementById("formulario");
  const formData = new FormData(form);

  const respuestas = [];
  for (let i = 0; i < 5; i++) {
    respuestas.push(parseInt(formData.get(`q${i}`)));
  }

  fetch("/resultado", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ respuestas: respuestas })
  })
  .then(response => response.text())
  .then(html => {
    document.open();
    document.write(html);
    document.close();
  });
}
