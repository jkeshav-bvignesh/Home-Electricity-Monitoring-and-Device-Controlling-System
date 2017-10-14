flag = 0;
		get_quota();
		get_details();
		getbuttonstate();
		setInterval(get_quota, 120000);
		function get_quota() {
			$.ajax({
					 url: "/getquota",
					 contentType: "application/json; charset=utf-8",
					 dataType: "json",
					 success: function (data) {
					 document.getElementById("currentValue").innerHTML = data["val"];
					}
				   });
		}
		
		function get_details() {
			url = "/getdetails";
			$.get(url,function(result){
			document.getElementById("name").value = result["username"];
			document.getElementById("phone").value = result["phone"];
			}
			);
		}

		
		function edit(){
			document.getElementById("savebutton").disabled = false;
			document.getElementById("name").readOnly = false;
			document.getElementById("phone").readOnly = false;
		}

		function save(){
			document.getElementById("savebutton").disabled = true;
			document.getElementById("name").readOnly = true;
			document.getElementById("phone").readOnly = true;
			
			uname = document.getElementById("name").value;
			phone = document.getElementById("phone").value;
			data = { 
					'username': uname,
					'phone': phone
			}; 
			url = "/setdetails";
			$.post(url, data, function(result){
				if(result['val'] == "1"){
					alert("Details Saved");
				}
						
				else{
					alert("Error while setting quota");
				}
			});
		}
		
		function set(){
			a = document.getElementById("usr").value;
			data = { 
					'quota': a
			}; 
			url = "/setnewquota";
			$.post(url, data, function(result){
				if(result['val'] == "1"){
					get_quota();
					alert("New Quota Set");
				}
						
				else{
					alert("Error while setting quota");
				}
			});
		
		}		

		function setbuttonstate(){
			flag = 1;
			b1 = document.getElementById("c1").checked;
			b2 = document.getElementById("c2").checked;
			b3 = document.getElementById("c3").checked;
			
			data = { 
					'b1': b1,
					'b2': b2,
					'b3': b3
			}; 
			
			url = "/setbuttonstate";
			
			$.post(url, data, function(result){
				if(result['val'] == "1"){
					console.log("button state send");
					flag = 0;
				}
						
				else{
					console.log("Error while sending state of buttons");
				}
			});
			
		}
		
		setInterval(getbuttonstate, 1000);
		function getbuttonstate(){
			b1 = true
			b2 = true
			b3 = true
			$.ajax({
					 url: "/getbuttonstate",
					 contentType: "application/json; charset=utf-8",
					 dataType: "json",
					 success: function (data) {
						if(flag != 1){
							 if( data['b1'] == "false"){
								b1 = false;
							 }
							 if( data['b2'] == "false"){
								b2 = false;
							 }
							 if( data['b3'] == "false"){
								b3 = false;
							 }
							 document.getElementById("c1").checked = b1;
							 document.getElementById("c2").checked = b2;
							 document.getElementById("c3").checked = b3;
						}
					}
				   });
		}