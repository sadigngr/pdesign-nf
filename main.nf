params.workingPath = "$baseDir"

params.chr1 = "Not Defined"
params.chr2 = "Not Defined"
params.skip_repeatMasker = false

def x = 1
def y = 2

log.info """\

		P R I M E R - D E S I G N
		
		Chromosome Files : 
		    ${params.chr1}
		    ${params.chr2}
"""

process MASK_SEQUENCES {

    input:
    path chr1
    path chr2
    
    output:
    stdout
    """
    echo "masked $chr1 $chr2"
    """
}

process RUN_NUCMER {

	input:
	path chrom1
	path chrom2
	
	output:
	path "output.coords"
	
	script:
	"""
	nucmer --prefix=output --coords  $chrom1 $chrom2
	"""
}

process PARSE_COORDS {
    
    input:
    path coordsfile
    
    output:
    path "parsed_output.txt"
    
    
    script:
    """
    awk -F'[|]' 'NF > 1 && \$0 !~ /^#/ {split(\$1,a," "); split(\$2,b," "); S1=a[1]; E1=a[2]; S2=b[1]; E2=b[2]; print S1, E1, S2, E2}' $coordsfile > parsed_output.txt
    """

}


process RUN_CLUSTALW {
    input:
    path chr1
    path chr2
    val parsedLocs


    output:
    path "*.aln"
    
    script:
    """
    python3 $baseDir/Extract.py $chr1 $chr2 $parsedLocs
    """
}


process PREPARE_FOR_PRIMER3{

    input:
    path clustalPath

    output:
    path "*.txt"

    """
    python3 $baseDir/autoprimer1.py $clustalPath
    """

}

process RUN_PRIMER3{
    input:
    path primerPath

    output:
    path "*seq1_output.txt"
    path "*seq2_output.txt"

    """
    python3 $baseDir/autoprimer2.py $primerPath
    """

}

process WRITE_PRIMERS{

    input:
    path writePath
    path writePath_1

    output:
    path "primer3_result_$x"
    path "primer3_result_$y"
    
    """
    python3 $baseDir/primer2.py $x $writePath && python3 $baseDir/primer2.py $y $writePath_1
    """

}

process MATCH_PRIMERS{

    input:
    path file1
    path file2

    output:
    path "matchedPrimers.txt"

    """
    python3 $baseDir/primermatch4.py $file1 $file2 > matchedPrimers.txt
    """

}



workflow{
        
    if ( !params.skip_repeatMasker ) {
    
    masked_paths_ch = MASK_SEQUENCES(params.chr1,params.chr2).view()
    
    nucmer_ch = RUN_NUCMER(params.chr1,params.chr2)
    
    }
    else {
    
    nucmer_ch = RUN_NUCMER(params.chr1,params.chr2) 
    
    }
	
    parse_ch = PARSE_COORDS(nucmer_ch).flatten()
    
    match_primers_ch = RUN_CLUSTALW(params.chr1,params.chr2,parse_ch) | PREPARE_FOR_PRIMER3 | RUN_PRIMER3 | WRITE_PRIMERS | MATCH_PRIMERS

    println("The Matched Primers Can Be Found On : ")
    match_primers_ch.view()
    
}
