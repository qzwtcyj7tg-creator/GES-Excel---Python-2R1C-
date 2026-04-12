    def _formatieren(self, datei: Path):
        wb = load_workbook(datei)
        ws = wb.active

        # Farben definieren
        green_fill = PatternFill(fill_type='solid', start_color='90EE90', end_color='90EE90')  # Hellgrün für 0
        light_orange_fill = PatternFill(fill_type='solid', start_color='FFF2CC', end_color='FFF2CC')  # Hellgelb/Orange für 0-0.3
        orange_fill = PatternFill(fill_type='solid', start_color='F4B183', end_color='F4B183')  # Orange für 0.3-1
        red_fill = PatternFill(fill_type='solid', start_color='FF6666', end_color='FF6666')  # Rot für >1

        header = [cell.value for cell in ws[1]]
        diff_spalten = []
        for i, name in enumerate(header, start=1):
            if isinstance(name, str):
                n = name.strip()
                if n.startswith('d') or n == 'Differenz Volumenstrom':
                    diff_spalten.append(i)

        for row in range(2, ws.max_row + 1):
            for col_idx in diff_spalten:
                cell = ws.cell(row=row, column=col_idx)
                try:
                    val = float(cell.value)
                    abs_val = abs(val)
                except (TypeError, ValueError):
                    continue

                # Farblogik
                if abs_val == 0:
                    cell.fill = green_fill
                elif abs_val <= 0.3:
                    cell.fill = light_orange_fill
                elif abs_val <= 1:
                    cell.fill = orange_fill
                elif abs_val > 1:
                    cell.fill = red_fill

        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = ws.dimensions
        wb.save(datei)

        def excel_erstellen(self, dateiname: Optional[str] = None) -> Path:
            df_py, df_ref, py_datei = self._daten_laden()
            result = self._aufbauen(df_py, df_ref)

            if not dateiname:
                dateiname = f'Validierung_{py_datei.stem}.xlsx'
            ziel = self.output_ordner / dateiname
            result.to_excel(ziel, index=False)
            self._formatieren(ziel)
            return ziel