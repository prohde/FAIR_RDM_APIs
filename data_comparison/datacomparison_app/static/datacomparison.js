document.addEventListener('DOMContentLoaded', function () {
    const classes_label = ['mr-2', 'text-xs', 'required'],
          classes_input_resources = ['mr-4', 'rounded-input'],
          new_resource = document.getElementById('datasets');

    let columns = [],
        data_ = [],
        dtTable = null,
        num_resources = 1;

    function openTab(btn, tabName) {
        document.querySelectorAll('.tabcontent').forEach(function (tc) {
            tc.style.display = 'none';
        });
        document.querySelectorAll('.tablinks').forEach(function (tl) {
            tl.classList.remove('active');
        });
        document.getElementById(tabName).style.display = 'block';
        btn.classList.add('active');
    }
    window.openTab = openTab;  // expose for inline onclick attributes

    document.getElementById('defaultOpen').click();  // open table tab by default

    function createLabel(text, htmlFor, classes) {
        let label = document.createElement('label');
        label.innerText = text;
        label.htmlFor = htmlFor;
        DOMTokenList.prototype.add.apply(label.classList, classes);
        return label;
    }

    function createInput(id_, type, placeholder, classes, required, size) {
        let input = document.createElement('input');
        DOMTokenList.prototype.add.apply(input.classList, classes);
        input.type = type;
        input.id = id_;
        input.name = id_;
        if (size !== null) { input.size = size; }
        input.placeholder = placeholder;
        input.required = required;
        return input;
    }

    function addNewResourceForm() {
        num_resources += 1;
        const submit_btn = document.getElementById('dataset_submit');
        submit_btn.remove();

        for (let i = 2; i < num_resources; i++) {
            // prevent changes to previous resources since they would be ignored
            document.getElementById('res' + i + 'label').disabled = true;
            if (i > 1) {
                const prevFile = document.getElementById('res' + i + 'file');
                if (prevFile) { prevFile.disabled = true; }
            }
        }

        const new_label_id = 'res' + num_resources + 'label',
              new_file_id= 'res' + num_resources + 'file';

        new_resource.append(document.createElement('br'));
        new_resource.append(document.createElement('br'));
        let heading = document.createElement('b');
        heading.innerText = 'Resource ' + num_resources;
        new_resource.append(heading);
        new_resource.append(document.createElement('br'));
        new_resource.append(createLabel('Label:', new_label_id, classes_label));
        new_resource.append(createInput(new_label_id, 'text', 'name', classes_input_resources, true, 20));

        // File input replaces the URL text input + datalist from the original
        new_resource.append(createLabel('File:', new_file_id, classes_label));
        let input_file = document.createElement('input');
        input_file.type = 'file';
        input_file.id = new_file_id;
        input_file.name = new_file_id;
        input_file.accept = '.csv,.tsv,.txt';
        input_file.style = 'width: 50ch;';
        DOMTokenList.prototype.add.apply(input_file.classList, classes_input_resources);
        new_resource.append(input_file);
        new_resource.append(submit_btn);
    }

    new_resource.onsubmit = function (event) {
        event.preventDefault();

        // Joins the file selected for `num_resources` into the existing dataset.
        function joinCurrentResource() {
            const res_new_file = document.getElementById('res' + num_resources + 'file'),
                  res_new_label = ' (' + document.getElementById('res' + num_resources + 'label').value + ')';

            if (!res_new_file || !res_new_file.files[0]) {
                alert('Please select a file for Resource ' + num_resources + '.');
                return;
            }

            Papa.parse(res_new_file.files[0], {
                skipEmptyLines: 'greedy',
                complete: function (results) {
                    let data_new = results.data,
                        columns_new = data_new.shift();

                    for (let i = 1; i < columns_new.length; i++) {
                        columns_new[i] = columns_new[i] + res_new_label;
                    }

                    const intersection = columns.filter(value => columns_new.includes(value));

                    if (1 === 1) {
                        const join_column = intersection[0],
                            idx_old = 0,
                            idx_new = 0,
                            num_cols_old = columns.length - 1,
                            num_cols_new = columns_new.length - 1;

                        let columns_copy = [...columns_new];
                        columns_copy.splice(idx_new, 1);
                        columns = columns.concat(columns_copy);

                        while (data_new.length > 0) {
                            let found  = false,
                                record = data_new.shift();

                            for (let i = 0; i < data_.length; i++) {
                                if (record[idx_new] == data_[i][idx_old]) {
                                    found = true;
                                    record.splice(idx_new, 1);

                                    let length = record.length;
                                    while (length < num_cols_new) {
                                        record.push(null);
                                        length++;
                                    }

                                    data_[i] = data_[i].concat(record);
                                    break;
                                }
                            }

                            if (!found) {
                                let record_old = Array(num_cols_old + 1).fill(null);
                                record_old[idx_old] = record[idx_new];
                                record.splice(idx_new, 1);
                                record = record_old.concat(record);
                                data_.push(record);
                            }
                        }

                        // Take care of old records which have not been updated yet
                        const num_cols = num_cols_old + num_cols_new + 1;
                        for (let i = 0; i < data_.length; i++) {
                            if (data_[i].length < num_cols) {
                                data_[i] = data_[i].concat(Array(num_cols - data_[i].length).fill(null));
                            }
                        }

                        addNewResourceForm();
                    } else {
                        console.log('There is either no or several matching column(s).');
                    }
                    updateUI();
                },
                error: function (err) { console.error(err); }
            });
        }

        if (num_resources === 1) {
            // First submit: load Resource 1 and display it alone.
            const res1file = document.getElementById('res1file');
            if (!res1file || !res1file.files[0]) {
                alert('Please select a file for Resource 1.');
                return;
            }

            Papa.parse(res1file.files[0], {
                skipEmptyLines: 'greedy',
                complete: function (results) {
                    columns = results.data[0];
                    data_ = results.data.slice(1);

                    const elem_res1_label = document.getElementById('res1label'),
                        res1_label = ' (' + elem_res1_label.value + ')';
                    for (let i = 1; i < columns.length; i++) {
                        columns[i] = columns[i] + res1_label;
                    }
                    elem_res1_label.disabled = true;
                    res1file.disabled = true;

                    addNewResourceForm();   // appends the Resource 2 row
                    updateUI();
                },
                error: function (err) { console.error(err); }
            });
        } else {
            joinCurrentResource();  // Subsequent submits: Resource 1 already in memory, join the new file
        }
    };

    function updateUI() {
        openTab(document.getElementById('defaultOpen'), 'table');

        document.getElementById('totalRows').textContent = data_.length.toLocaleString() + ' row' + (data_.length !== 1 ? 's' : '');

        if (dtTable) {
            dtTable.destroy();
            document.getElementById('comparison-table').innerHTML = '';
        }

        // DataTables 2.x — works with or without jQuery
        dtTable = new DataTable('#comparison-table', {
            data:       data_,
            columns:    columns.map(function (c, i) {
                return { title: c, data: i, defaultContent: '' };
            }),
            pageLength: 25,
            scrollX:    true,
            layout: {
                topStart:    'searchBuilder',
                topEnd:      'search',
                bottomStart: ['info', 'pageLength'],
                bottomEnd:   'paging'
            }
        });

        populateChartControls();
    }

    function populateChartControls() {
        const xAxisSel = document.getElementById('xAxis'),
              yAxisWrap = document.getElementById('yAxis');
        xAxisSel.innerHTML = '';
        yAxisWrap.innerHTML = '';

        columns.forEach(function (col, i) {
            const opt       = document.createElement('option');
            opt.value = i;
            opt.textContent = col;
            xAxisSel.appendChild(opt);

            const lbl        = document.createElement('label');
            lbl.className = 'block font-bold text-white';
            const chk        = document.createElement('input');
            chk.type = 'checkbox';
            chk.className = 'ml-0 mr-2 leading-tight';
            chk.value = i;
            chk.name = 'ySeries';
            chk.checked = (i === 0);
            const span = document.createElement('span');
            span.className = 'text-xs';
            span.textContent = col;
            lbl.appendChild(chk);
            lbl.appendChild(span);
            yAxisWrap.appendChild(lbl);
        });
    }

    document.getElementById('chartBuilder').addEventListener('submit', function (e) {
        e.preventDefault();
        renderChart();
    });

    function renderChart() {
        if (!columns.length) { return; }

        const chartType = document.getElementById('chartType').value,
              xAxisIdx = parseInt(document.getElementById('xAxis').value),
              useLog = document.getElementById('logScale').checked,
              useFiltered = document.getElementById('filteredData').checked;

        const yIndices = Array.from(
            document.querySelectorAll('#yAxis input[type="checkbox"]:checked')
        ).map(function (cb) { return parseInt(cb.value); });

        if (!yIndices.length) { return; }

        const plotRows = (useFiltered && dtTable)
            ? dtTable.rows({ search: 'applied' }).data().toArray()
            : data_;

        if (!plotRows.length) { return; }

        const xValues = plotRows.map(function (row) { return row[xAxisIdx]; });

        const palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'];

        const traces = yIndices.map(function (yIdx, ti) {
            const yValues = plotRows.map(function (row) {
                const v = parseFloat(row[yIdx]);
                return isNaN(v) ? null : v;
            });
            const color = palette[ti % palette.length];
            const base = {
                x: xValues, y: yValues, name: columns[yIdx],
                marker: { color: color }, line: { color: color }
            };
            if (chartType === 'scatter') {
                return Object.assign({}, base, { type: 'scatter', mode: 'markers' });
            }
            if (chartType === 'line') {
                return Object.assign({}, base, { type: 'scatter', mode: 'lines', line: { 'shape': 'spline', 'smoothing': 1.3 } });
            }
            return Object.assign({}, base, { type: 'bar' });
        });

        const layout = {
            xaxis: { autorange: true },
            yaxis: { type: useLog ? 'log' : '-', autorange: true },
            uirevision:'true',
            barmode: chartType === 'bar' ? 'group' : undefined,
            margin: { t: 30 },
            hovermode: 'x unified'
        };

        const guide = document.getElementById('guidingText');
        if (guide) { guide.style.display = 'none'; }

        Plotly.react('gd', traces, layout, { responsive: true, displaylogo: false });
    }

}); // end DOMContentLoaded
