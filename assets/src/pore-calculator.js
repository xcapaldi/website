function calculateSize() {
    // solution conductivity
    if (isNaN(document.getElementById('conductivity').value)) {
	var conductivity = 0;
    } else {
	if (document.getElementById('S_m').checked) {
	    var conductivity = parseFloat(document.getElementById('conductivity').value);
	} else {
	    var conductivity = parseFloat(document.getElementById('conductivity').value) / 10;
	}
    }

    if (isNaN(document.getElementById('err_conductivity').value)) {
	var err_conductivity = 0;
    } else {
	if (document.getElementById('S_m').checked) {
	    var err_conductivity = parseFloat(document.getElementById('err_conductivity').value);
	} else {
	    var err_conductivity = parseFloat(document.getElementById('err_conductivity').value) / 10;
	}
    }

    // effective length
    if (isNaN(document.getElementById('length').value)) {
	var length = 0;
    } else {
	var length = parseFloat(document.getElementById('length').value) * (10 ** -9);
    }

    if (isNaN(document.getElementById('err_length').value)) {
	var err_length = 0;
    } else {
	var err_length = parseFloat(document.getElementById('err_length').value) * (10 ** -9);
    }

    // pore conductance
    if (isNaN(document.getElementById('conductance').value)) {
	var conductance = 0;
    } else {
	if (document.getElementById('A_V').checked) {
	    var conductance = parseFloat(document.getElementById('conductance').value);
	} else if (document.getElementById('pA_mV').checked) {
	    var conductance = parseFloat(document.getElementById('conductance').value) * (10 ** -12) * (1000);
	} else {
	    var conductance = parseFloat(document.getElementById('conductance').value) * (10 ** -9) * (1000);
	}
    }

    if (isNaN(document.getElementById('err_conductance').value)) {
	var err_conductance = 0;
    } else {
	if (document.getElementById('A_V').checked) {
	    var err_conductance = parseFloat(document.getElementById('err_conductance').value);
	} else if (document.getElementById('pA_mV').checked) {
	    var err_conductance = parseFloat(document.getElementById('err_conductance').value) * (10 ** -12) * (1000);
	} else {
	    var err_conductance = parseFloat(document.getElementById('err_conductance').value) * (10 ** -9) * (1000);
	}
    }

    // channel conductance
    if (isNaN(document.getElementById('ch_conductance').value)) {
	var ch_conductance = 0;
    } else {
	if (document.getElementById('ch_A_V').checked) {
	    var ch_conductance = parseFloat(document.getElementById('ch_conductance').value);
	} else if (document.getElementById('ch_pA_mV').checked) {
	    var ch_conductance = parseFloat(document.getElementById('ch_conductance').value) * (10 ** -12) * (1000);
	} else {
	    var ch_conductance = parseFloat(document.getElementById('ch_conductance').value) * (10 ** -9) * (1000);
	}
    }

    if (isNaN(document.getElementById('err_ch_conductance').value)) {
	var err_ch_conductance = 0;
    } else {
	if (document.getElementById('ch_A_V').checked) {
	    var err_ch_conductance = parseFloat(document.getElementById('err_ch_conductance').value);
	} else if (document.getElementById('ch_pA_mV').checked) {
	    var err_ch_conductance = parseFloat(document.getElementById('err_ch_conductance').value) * (10 ** -12) * (1000);
	} else {
	    var err_ch_conductance = parseFloat(document.getElementById('err_ch_conductance').value) * (10 ** -9) * (1000);
	}
    }

    // double electrode
    if (document.getElementById('double_electrode').checked) {
	var double_electrode = true;
    } else {
	var double_electrode = false;
    }

    // estimate the diameter
    // assume channel and pore resistances act as resistors in series
    // remember that we only need 0.5 * the measured channel resistance
    if (ch_conductance > 0) {
	if (double_electrode) {
	    var branch_conductance = 4 * ch_conductance;
	    var err_branch = err_ch_conductance / 4;
	} else {
	    var branch_conductance = 2 * ch_conductance;
	    var err_branch = err_ch_conductance / 2;
	}

	var pore_conductance = (((conductance ** -1) - (branch_conductance ** -1)) ** -1);
	var err_pore = (pore_conductance * (Math.sqrt((((err_conductance)/(conductance ** 2))**2)+(((err_branch)/(branch_conductance ** 2)) ** 2)))/((err_conductance ** -1) - (err_branch ** -1)));
    } else {
	// otherwise just treat it simply
	pore_conductance = conductance;
	err_pore = err_conductance;
    }

    var K = Math.sqrt(1 + ((16*conductivity*length)/(Math.PI*pore_conductance)))

    var diameter = (pore_conductance / (2*conductivity)) * (1 + K)

    var err_diameter = Math.sqrt(((((1+K)/(2*conductivity))-((4*length)/(Math.PI*pore_conductance*K)))**2)*err_pore**2+((((4*length)/(Math.PI*conductivity*K))-((pore_conductance/(2*conductivity**2))*(1+K)))**2)*err_conductivity**2+((4/(Math.PI*K))**2)*err_length**2)

    var nm_diameter = (diameter * (10 ** 9)).toPrecision(4);
    var nm_err_diameter = (err_diameter * (10 ** 9)).toPrecision(4);

    // display the result
    document.getElementById('diameter').innerHTML = nm_diameter + ' ± ' + nm_err_diameter + ' nm';
}
