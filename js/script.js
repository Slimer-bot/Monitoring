var getCellValue = function(tr, idx){ return tr.children[idx].innerText || tr.children[idx].textContent; }

var comparer = function(idx, asc) { return function(a, b) { return function(v1, v2) {
        return v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2);
    }(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));
}};

// do the work...
Array.prototype.slice.call(document.querySelectorAll('th')).forEach(function(th) { th.addEventListener('click', function() {
        const table = th.closest('table');
		const tbody = table.querySelector('tbody');
		Array.from(tbody.querySelectorAll('tr'))
			.sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
			.forEach(tr => tbody.appendChild(tr) );
    })
});
function f1(objButton){ 
	
	let arrayObj = objButton.value.split('\n');
	swal("About error", arrayObj.join('\n*'));

}

