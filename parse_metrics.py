#!/usr/bin/env python
import re, sys, os
import sqlite3
import datetime

class Metrics:
    hsmetrics_targets = ['TOTAL_READS', 'PCT_PF_UQ_READS', 'PCT_PF_UQ_READS_ALIGNED', 'PCT_OFF_BAIT', 'MEAN_TARGET_COVERAGE',
               'ZERO_CVG_TARGETS_PCT', 'PCT_TARGET_BASES_2X', 'PCT_TARGET_BASES_30X', 'PCT_TARGET_BASES_100X']

    def __init__(self, ifile):
        self.name = re.sub('_hsmetrics.txt', '', os.path.basename(ifile))
        self.hslist = []
        self.sequencer = 'Hiseq2500'
        self.sampleDate = datetime.date.today().isoformat()
        self.projectId = 'Project1'
        self.user_id = 'paddy'

    def add_hsmetrics(self, ifile):
        with open(ifile) as f:
            for line in f:
                line = line.rstrip()
                if line.startswith('BAIT_SET'):
                    word = line.split('\t')
                elif line.startswith('SeqCap_EZ_Exome_v2_target_interval'):
                    word2 = line.split('\t')
        for i in range(0, len(word)-3):
            if word[i] in self.hsmetrics_targets:
                self.hslist.append(word2[i])
        self.hslist.append(self.name)
        return self.hslist

    def upload_hsmetrics(self):
        conn = sqlite3.connect('/Users/patricklombard/Documents/2017/django_project/ngs_quality/db.sqlite3')
        c = conn.cursor()
        #c.execute("INSERT INTO quality_metrics_sampleInfo(projectId, sampleId, sampleDate, sampleSequencer, user_id) VALUES(?,?,?,?,?)",
         #       [self.projectId, self.name, self.sampleDate, self.sequencer, self.user_id])
        c.execute("INSERT INTO quality_metrics_hsmetrics(total_reads, pct_uq_reads, pct_uq_reads_aligned, pct_off_bait, mean_target_coverage, \
               zero_cvg_targets_pct, pct_target_bases_2x, pct_target_bases_30x,pct_target_bases_100x, sample_id) \
               VALUES (?,?,?,?,?,?,?,?,?,(SELECT id FROM quality_metrics_sampleInfo WHERE quality_metrics_sampleInfo.sampleId = ? ))", self.hslist)
        conn.commit()
        conn.close()
 #You could extend this by adding FastQC results for this sample

def main():
    ifiles = [f for f in os.listdir('data/') if f.endswith('.txt')]
    for i in ifiles:
        m = Metrics(i)
        m.add_hsmetrics('data/'+i)
        m.upload_hsmetrics()


main()