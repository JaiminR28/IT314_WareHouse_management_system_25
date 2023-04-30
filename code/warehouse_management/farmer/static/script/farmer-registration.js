"use strict";

const startDateEl = document.getElementById("startDate");
const endDateEl = document.getElementById("endDate");
const endDateBlock = document.getElementById("endDateBlck");

endDateEl.disabled = true;

let date = new Date();

let tdate = date.getDate();
let month = date.getMonth() + 1;
let year = date.getUTCFullYear();

if (tdate < 10) {
	tdate = "0" + tdate;
}

if (month < 10) {
	month = "0" + month;
}

let startDate = year + "-" + month + "-" + tdate;
startDateEl.setAttribute("min", startDate);

startDateEl.addEventListener("change", function () {
	const checkvalue = $("#startDate").val();
	if (checkvalue) {
		console.log(checkvalue);
		endDateEl.disabled = false;
	}
});

endDateEl.addEventListener("click", function () {
	const endDate = $("#startDate").val();
	if (endDate !== null) {
		endDateEl.setAttribute("min", endDate);
	}
});

endDateBlock.addEventListener("mouseover", function () {
	console.log("move");
	const checkvalue = $("#startDate").val();
	if (checkvalue) {
		console.log(checkvalue);
		endDateEl.disabled = false;
	} else {
		endDateEl.disabled = true;
	}
});
