const BASE_URL = "http://127.0.0.1:5000/api"

/* generating HTML for an individual cupcake */

function generateCupcakeHTML(cupcake) {
    return `
        <div data-cupcake-id=${cupcake.id} class="col-sm-3">
            <h2>${cupcake.flavor}</h2>
            <p>size: ${cupcake.size} / rating: ${cupcake.rating}</p>
            <img class="Cupcake-img"
                src="${cupcake.image}"
                alt="(no image provided)"
                width="200">
            <button class="delete-button btn m-3">Delete</button>
        </div>
    `;
  }

  /** loading the initial cupcakes on homepage. */

async function showInitialCupcakes() {
    const res = await axios.get(`${BASE_URL}/cupcakes`);
 
    for (let cupcakeData of res.data.cupcakes) {
      let cupcakeHTML = $(generateCupcakeHTML(cupcakeData));
      $("#cupcakes-section").append(cupcakeHTML);
    }
  }

/** handle cupcake adding form  */

$("#add-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
  
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();
  
    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
      flavor,
      rating,
      size,
      image
    });
  
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-section").append(newCupcake);
    $("#add-cupcake-form").trigger("reset");
  });
  


/** handles the delete cupcake button */

$("#cupcakes-section").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
})


/** run showInitialCupcakes function */

$(showInitialCupcakes);
