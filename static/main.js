function fetchExistingConfigurations() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
        var configurations = JSON.parse(this.responseText);
        populateDeviceTable(configurations);
      }
    };
    xhttp.open("GET", "/get_configurations", true); 
    xhttp.send();
  }

  function populateDeviceTable(configurations) {
    var table = document.getElementById("deviceTable");
    for (var i = 0; i < configurations.length; i++) {
      var deviceID = configurations[i].deviceID;
      var address = configurations[i].address;

      var row = table.insertRow(-1);
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row.insertCell(2);
      var cell4 = row.insertCell(3);

      cell1.innerHTML = deviceID;
      cell2.innerHTML = address;
      cell3.innerHTML = '<button onclick="editDevice(this)">Edit</button>';
      cell4.innerHTML = '<button onclick="deleteDevice(this)">Delete</button>';
    }
  }
    function addDevice(event) {
      event.preventDefault(); 

      var deviceID = document.getElementById("deviceID").value;
      var address = document.getElementById("address").value;

      if (deviceID === "" || address === "") {
        alert("Please enter both Device ID and Address.");
        return;
      }

      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
          var response = JSON.parse(this.responseText);
          if (response.success) {
            document.getElementById("deviceForm").reset();
            addDeviceToTable(deviceID, address);
          } else {
            alert("Failed to add device configuration.");
          }
        }
      };
      xhttp.open("POST", "/add_device", true);
      xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      xhttp.send("deviceID=" + encodeURIComponent(deviceID) + "&address=" + encodeURIComponent(address));
    }

    function addDeviceToTable(deviceID, address) {
      var table = document.getElementById("deviceTable");
      var row = table.insertRow(-1);
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row.insertCell(2);
      var cell4 = row.insertCell(3);

      cell1.innerHTML = deviceID;
      cell2.innerHTML = address;
      cell3.innerHTML = '<button onclick="editDevice(this)">Edit</button>';
      cell4.innerHTML = '<button onclick="deleteDevice(this)">Delete</button>';
    }

    function editDevice(button) {
      var row = button.parentNode.parentNode;
      var deviceID = row.cells[0].innerHTML;
      var address = row.cells[1].innerHTML;
    
      var newDeviceID = prompt("Enter the new Device ID:", deviceID);
      var newAddress = prompt("Enter the new Address:", address);
    
      if (newDeviceID && newAddress) {
        row.cells[0].innerHTML = newDeviceID;
        row.cells[1].innerHTML = newAddress;
    
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState === 4 && this.status === 200) {
            var response = JSON.parse(this.responseText);
            if (response.success) {
              alert("Device configuration updated successfully.");
            } else {
              alert("Failed to update device configuration.");
            }
          }
        };
        xhttp.open("POST", "/edit_device", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("deviceID=" + encodeURIComponent(deviceID) + "&newDeviceID=" + encodeURIComponent(newDeviceID) + "&address=" + encodeURIComponent(newAddress));
      }
    }
    
    
function deleteDevice(button) {
  var row = button.parentNode.parentNode;
  var deviceID = row.cells[0].innerHTML;

  if (confirm("Are you sure you want to delete the device configuration for Device ID: " + deviceID + "?")) {
    row.remove();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
        var response = JSON.parse(this.responseText);
        if (response.success) {
          alert("Device configuration deleted successfully.");
        } else {
          alert("Failed to delete device configuration.");
        }
      }
    };
    xhttp.open("POST", "/delete_device", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("deviceID=" + encodeURIComponent(deviceID));
  }
}
  
    function showConfigurationList() {
    window.location.href = "/";
    }

    function showDashboard() {
      window.location.href = "/dashboard";
    }

    
    
    window.onload = function() {
    fetchExistingConfigurations();
  };