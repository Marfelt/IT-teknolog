function updateVisualizer(bin_id, percentageData) {
  var visualizer = document.getElementById("visualizer-" + bin_id);
  var percentage = visualizer.querySelector(".trash-percentage");
  percentage.textContent = percentageData + "%";

  var containerLiquid = visualizer.querySelector(".container__liquid");

  if (percentageData <= 30) {
    containerLiquid.style.background = 'var(--gradient-color-green)';
  } else if (percentageData <= 60) {
    containerLiquid.style.background = 'var(--gradient-color-yellow)';
  } else if (percentageData <= 90) {
    containerLiquid.style.background = 'var(--gradient-color-orange)';
  } else {
    containerLiquid.style.background = 'var(--gradient-color-red)';
  }
}

var formButtonsVisible = false;

function toggleFormButtons() {
  formButtonsVisible = !formButtonsVisible; 

  var formButtons = document.getElementsByClassName("form-button");

  for (var i = 0; i < formButtons.length; i++) {
    if (formButtonsVisible) {
      formButtons[i].style.display = "block"; 
    } else {
      formButtons[i].style.display = "none"; 
    }
  }
}

toggleFormButtons();

function createVisualizer(bin_id, percentageData) {
  var visualizerContainer = document.getElementById("visualizerContainer");

  var existingVisualizer = document.getElementById("visualizer-" + bin_id);
  if (existingVisualizer) {
    saveContainerOrder();
    updateVisualizer(bin_id, percentageData);
    return;
  }

  var visualizer = document.createElement("div");
  visualizer.id = "visualizer-" + bin_id;
  visualizer.classList.add("container__wrapper");

  var iconContainer = document.createElement("div");
  iconContainer.classList.add("container__icon");

  var levelContainer = document.createElement("div");
  levelContainer.classList.add("container__level");

  var liquid = document.createElement("div");
  liquid.classList.add("container__liquid");

  var containerHeight = 180; 
  var liquidHeight = Math.round((containerHeight * percentageData) / 100);
  liquid.style.height = liquidHeight + "px"; 

  levelContainer.appendChild(liquid);
  iconContainer.appendChild(levelContainer);

  visualizer.appendChild(iconContainer);

  var percentageText = document.createElement("div");
  percentageText.classList.add("trash-percentage");
  percentageText.textContent = percentageData + "%";

  visualizer.appendChild(percentageText);

  var formButton = document.createElement("button");
  formButton.classList.add("form-button");
  formButton.textContent = "...";
  formButton.addEventListener("click", function() {
    openForm(bin_id);
  });

  visualizer.appendChild(formButton);

  visualizerContainer.appendChild(visualizer);
}

function openForm(bin_id) {
  var modalOverlay = document.createElement("div");
  modalOverlay.classList.add("modal-overlay");

  var formContainer = document.createElement("div");
  formContainer.classList.add("form-container");

  var form = document.createElement("form");
  form.classList.add("bin-form");

  var binIdElement = document.createElement("span");
  binIdElement.classList.add("bin-id");
  binIdElement.textContent = "Bin ID: " + bin_id;

  var closeButton = document.createElement("button");
  closeButton.classList.add("close-button");
  closeButton.textContent = "X";
  closeButton.addEventListener("click", function() {
    closeModal(modalOverlay);
  });

  var deleteButton = document.createElement("button");
  deleteButton.classList.add("delete-button");
  deleteButton.textContent = "Delete";
  deleteButton.addEventListener("click", function() {
    deleteBin(bin_id);
    closeModal(modalOverlay);
  });

  form.appendChild(binIdElement);
  form.appendChild(closeButton);
  form.appendChild(deleteButton);

  formContainer.appendChild(form);
  modalOverlay.appendChild(formContainer);
  document.body.appendChild(modalOverlay);
}

function closeModal(modalOverlay) {
  if (modalOverlay) {
    modalOverlay.remove();
  }
}

function sortContainerIcons() {
  var visualizerContainer = document.getElementById("visualizerContainer");
  var icons = Array.from(visualizerContainer.getElementsByClassName("container__wrapper"));

  icons.sort(function(a, b) {
    var binIdA = parseInt(a.getAttribute("data-bin-id").replace("Bin", ""));
    var binIdB = parseInt(b.getAttribute("data-bin-id").replace("Bin", ""));
    return binIdA - binIdB;
  });

  icons.forEach(function(icon) {
    visualizerContainer.appendChild(icon);
  });
}

function saveContainerOrder() {
  var visualizerContainer = document.getElementById("visualizerContainer");
  var icons = visualizerContainer.getElementsByClassName("container__wrapper");
  var order = [];

  for (var i = 0; i < icons.length; i++) {
    var binId = icons[i].getAttribute("data-bin-id");
    order.push(binId);
  }

  localStorage.setItem("containerOrder", JSON.stringify(order));
}

function restoreContainerOrder() {
  var visualizerContainer = document.getElementById("visualizerContainer");
  var order = localStorage.getItem("containerOrder");

  if (order) {
    order = JSON.parse(order);

    for (var i = 0; i < order.length; i++) {
      var binId = order[i];
      var icon = document.querySelector("[data-bin-id='" + binId + "']");
      visualizerContainer.appendChild(icon);
    }
  }
}

function deleteBin(bin_id) {
  var visualizer = document.getElementById("visualizer-" + bin_id);
  if (visualizer) {
    visualizer.remove();
  }

  var form = document.querySelector(".bin-form");
  if (form) {
    form.remove();
  }

  localStorage.removeItem("visualizerData-" + bin_id);
}



function createTrashBinVisualizer() {
  var bin_id = prompt("Enter the bin ID:");
  if (!bin_id) {
    return; 
  }

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      var percentageData = JSON.parse(this.responseText);

      createVisualizer(bin_id, percentageData);

      var visualizerData = {
        bin_id: bin_id,
        percentageData: percentageData
      };
      localStorage.setItem("visualizerData-" + bin_id, JSON.stringify(visualizerData));
    }
  };
  xhttp.open("GET", "/get_percentage_data?bin=" + encodeURIComponent(bin_id), true);
  xhttp.send();
}

function removeVisualizer(bin_id) {
  var visualizer = document.getElementById("visualizer-" + bin_id);
  if (visualizer) {
    visualizer.remove();
    localStorage.removeItem("visualizerData-" + bin_id);
  }
}


window.onload = function() {
  var visualizerDataList = [];
  for (var i = 0; i < localStorage.length; i++) {
    var key = localStorage.key(i);
    if (key.startsWith("visualizerData-")) {
      var visualizerData = JSON.parse(localStorage.getItem(key));
      visualizerDataList.push(visualizerData);
    }
  }

  visualizerDataList.sort(function(a, b) {
    var binIdA = parseInt(a.bin_id.replace("Bin", ""));
    var binIdB = parseInt(b.bin_id.replace("Bin", ""));
    return binIdA - binIdB;
  });

  visualizerDataList.forEach(function(visualizerData) {
    createVisualizer(visualizerData.bin_id, visualizerData.percentageData);
    fetchLatestPercentageData(visualizerData.bin_id);
  });

  restoreContainerOrder();
};

function fetchLatestPercentageData(bin_id) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      var percentageData = JSON.parse(this.responseText);
      updateVisualizer(bin_id, percentageData);

      var visualizerData = {
        bin_id: bin_id,
        percentageData: percentageData
      };
      localStorage.setItem("visualizerData-" + bin_id, JSON.stringify(visualizerData));
    }
  };
  xhttp.open("GET", "/get_latest_percentage_data?bin=" + encodeURIComponent(bin_id), true);
  xhttp.send();
}