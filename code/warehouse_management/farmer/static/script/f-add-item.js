"use strict";

const minTempEl = document.getElementById("minTemp");
const maxTempEl = document.getElementById("maxTemp");
const SubmitBtnEl = document.getElementById("submit");

maxTempEl.disabled = true;

console.log("");
minTempEl.addEventListener("change", function () {
	console.log($("#minTemp").val());
	const minTemp = $("#minTemp").val();

	if (minTemp) {
		maxTempEl.disabled = false;
		maxTempEl.min = minTemp;
	}
});
