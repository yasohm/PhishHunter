import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

const FEATURE_LABELS = {
    has_https: 'Protocole HTTPS',
    has_ip_address: 'Adresse IP dans URL',
    url_length: "Longueur de l'URL",
    has_at_symbol: 'Symbole @ présent',
    double_slash_redirect: 'Redirection double slash',
    prefix_suffix: 'Préfixe/Suffixe dans domaine',
    subdomain_count: 'Nombre de sous-domaines',
    ssl_state: 'Certificat SSL',
    domain_registration_length: "Durée d'enregistrement",
    favicon: 'Favicon externe',
    port: 'Port non standard',
    https_token: 'Token HTTPS dans domaine',
    request_url: 'Ressources externes',
    url_of_anchor: 'Ancres externes',
    links_in_tags: 'Liens dans balises meta/script',
    sfh: 'Action de formulaire',
    submitting_to_email: 'Soumission par email',
    abnormal_url: 'URL anormale',
    redirect: 'Nombre de redirections',
    on_mouseover: 'Modification status bar',
    rightclick: 'Clic droit désactivé',
    popup_window: 'Fenêtre popup',
    iframe: 'iFrame présent',
    domain_age: 'Âge du domaine',
    dns_record: 'Enregistrement DNS',
    web_traffic: 'Trafic web',
    page_rank: 'PageRank',
    google_index: 'Indexé par Google',
    links_pointing_to_page: 'Liens entrants',
    statistical_report: 'Rapport statistique',
    ratio_urls_suspectes: 'Ratio URLs suspectes',
    has_link_text_mismatch: 'Texte/lien différent',
    has_urgent_keywords: "Mots d'urgence",
    nb_mots_urgence: "Nombre mots d'urgence",
    subject_entropy: 'Entropie du sujet',
    has_html_form: 'Formulaire HTML',
    has_password_field: 'Champ mot de passe',
    has_brand_spoofing: 'Usurpation de marque',
    special_chars_subject: 'Caractères spéciaux (sujet)',
    has_free_email_sender: 'Email gratuit (expéditeur)',
};

const RISK_COLORS = {
    safe: [22, 163, 74],
    suspicious: [234, 88, 12],
    dangerous: [220, 38, 38],
};

const RISK_LABELS = {
    safe: 'SÛRE',
    suspicious: 'SUSPECTE',
    dangerous: 'DANGEREUSE',
};

function formatValue(value) {
    if (value === 1) return 'Oui';
    if (value === 0) return 'Non';
    if (value === -1) return 'Suspect';
    if (typeof value === 'number') return String(Math.round(value * 100) / 100);
    return String(value);
}

function isSuspect(value) {
    return value === -1 || value === 1;
}

export function exportJSON(data, filename = 'rapport-phishguard') {
    const report = {
        generator: 'PhishGuard',
        version: '1.0.0',
        generated_at: new Date().toISOString(),
        ...data,
    };
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `phishguard-${filename}-${data.scan_id || Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

export function exportPDF(data, type = 'url') {
    const doc = new jsPDF();
    const pageW = doc.internal.pageSize.getWidth();
    const m = 18;

    // Header band
    doc.setFillColor(15, 23, 42);
    doc.rect(0, 0, pageW, 36, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(18);
    doc.text('PhishGuard', m, 14);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.text('Rapport de Sécurité — Détection de Phishing', m, 23);
    doc.setFontSize(8);
    doc.text(new Date().toLocaleString('fr-FR'), pageW - m, 23, { align: 'right' });

    let y = 48;

    // Scan meta
    doc.setTextColor(100, 116, 139);
    doc.setFontSize(8);
    const scanDate = data.created_at
        ? new Date(data.created_at).toLocaleString('fr-FR')
        : new Date().toLocaleString('fr-FR');
    doc.text(`Scan #${data.scan_id || 'N/A'}  •  ${scanDate}`, m, y);
    y += 10;

    // Risk banner
    const riskColor = RISK_COLORS[data.risk_level] || RISK_COLORS.dangerous;
    doc.setFillColor(...riskColor);
    doc.roundedRect(m, y, pageW - m * 2, 22, 3, 3, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(12);
    const verdict = `${RISK_LABELS[data.risk_level] || 'INCONNUE'} — ${data.is_phishing ? 'Phishing Détecté' : 'Légitime'}`;
    doc.text(verdict, pageW / 2, y + 9, { align: 'center' });
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.text(`Niveau de confiance : ${data.confidence}%`, pageW / 2, y + 17, { align: 'center' });
    y += 30;

    // Target info
    doc.setTextColor(15, 23, 42);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(10);

    if (type === 'url') {
        doc.text("URL Analysée", m, y);
        y += 5;
        doc.setDrawColor(226, 232, 240);
        doc.line(m, y, pageW - m, y);
        y += 6;
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8);
        doc.setTextColor(71, 85, 105);
        const lines = doc.splitTextToSize(data.url || '', pageW - m * 2);
        doc.text(lines, m, y);
        y += lines.length * 5 + 10;
    } else {
        doc.text("Informations de l'Email", m, y);
        y += 5;
        doc.setDrawColor(226, 232, 240);
        doc.line(m, y, pageW - m, y);
        y += 6;
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8);
        doc.setTextColor(71, 85, 105);
        const subjectLines = doc.splitTextToSize(`Sujet : ${data.sujet || 'N/A'}`, pageW - m * 2);
        doc.text(subjectLines, m, y);
        y += subjectLines.length * 5 + 4;
        doc.text(`Expéditeur : ${data.expediteur || 'Inconnu'}`, m, y);
        y += 12;
    }

    // Features table
    doc.setTextColor(15, 23, 42);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(10);
    doc.text('Caractéristiques Analysées', m, y);
    y += 4;

    const features = data.features || {};
    const rows = Object.entries(features)
        .filter(([key]) => !key.endsWith('_UCI'))
        .map(([key, value]) => [
            FEATURE_LABELS[key] || key,
            formatValue(value),
            isSuspect(value) ? 'Suspect' : 'Normal',
        ]);

    autoTable(doc, {
        startY: y + 2,
        head: [['Caractéristique', 'Valeur', 'Statut']],
        body: rows,
        margin: { left: m, right: m },
        headStyles: {
            fillColor: [15, 23, 42],
            textColor: [255, 255, 255],
            fontSize: 8,
            fontStyle: 'bold',
        },
        bodyStyles: { fontSize: 8, textColor: [71, 85, 105] },
        alternateRowStyles: { fillColor: [248, 250, 252] },
        columnStyles: {
            0: { cellWidth: 95 },
            1: { cellWidth: 38, halign: 'center' },
            2: { cellWidth: 32, halign: 'center' },
        },
        didParseCell(data) {
            if (data.section === 'body' && data.column.index === 2 && data.cell.raw === 'Suspect') {
                data.cell.styles.fillColor = [254, 226, 226];
                data.cell.styles.textColor = [185, 28, 28];
                data.cell.styles.fontStyle = 'bold';
            }
        },
    });

    // URLs section for emails
    if (type === 'email' && data.url_analyses && data.url_analyses.length > 0) {
        const afterTable = doc.lastAutoTable.finalY + 12;
        doc.setTextColor(15, 23, 42);
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(10);
        doc.text('URLs Détectées et Analysées', m, afterTable);

        const urlRows = data.url_analyses.map((u) => [
            u.url,
            `${u.confidence}%`,
            RISK_LABELS[u.risk_level] || u.risk_level.toUpperCase(),
        ]);

        autoTable(doc, {
            startY: afterTable + 4,
            head: [['URL', 'Confiance', 'Verdict']],
            body: urlRows,
            margin: { left: m, right: m },
            headStyles: {
                fillColor: [15, 23, 42],
                textColor: [255, 255, 255],
                fontSize: 8,
                fontStyle: 'bold',
            },
            bodyStyles: { fontSize: 7, textColor: [71, 85, 105] },
            alternateRowStyles: { fillColor: [248, 250, 252] },
            columnStyles: {
                0: { cellWidth: 115 },
                1: { cellWidth: 25, halign: 'center' },
                2: { cellWidth: 25, halign: 'center' },
            },
            didParseCell(data) {
                if (data.section === 'body' && data.column.index === 2) {
                    if (data.cell.raw === 'DANGEREUSE') {
                        data.cell.styles.textColor = [185, 28, 28];
                        data.cell.styles.fontStyle = 'bold';
                    } else if (data.cell.raw === 'SUSPECTE') {
                        data.cell.styles.textColor = [154, 52, 18];
                        data.cell.styles.fontStyle = 'bold';
                    } else {
                        data.cell.styles.textColor = [22, 101, 52];
                        data.cell.styles.fontStyle = 'bold';
                    }
                }
            },
        });
    }

    // Footer on every page
    const total = doc.internal.getNumberOfPages();
    for (let i = 1; i <= total; i++) {
        doc.setPage(i);
        doc.setFontSize(7);
        doc.setTextColor(148, 163, 184);
        doc.text(
            `PhishGuard — Rapport généré automatiquement — Page ${i}/${total}`,
            pageW / 2,
            doc.internal.pageSize.getHeight() - 8,
            { align: 'center' }
        );
    }

    const prefix = type === 'email' ? 'email' : 'url';
    doc.save(`phishguard-${prefix}-#${data.scan_id || Date.now()}.pdf`);
}
