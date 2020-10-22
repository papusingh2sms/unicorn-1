#!/usr/bin/env ruby

Signal.trap("INT") {
    abort()
}

lhost = ARGV[0]
lport = ARGV[1]

if lhost == "none" or lhost == nil
    lhost = ""
end
if lport == "none" or lport == nil
    lport = ""
end

if 1
    if lhost.length >= 12 or lport.length >= 12
        if lhost.length >= lport.length
            stf = " " * (lhost.length - 3)
            fts = lhost.length + 2
        end
        if lport.length >= lhost.length
            stf = " " * (lport.length - 3)
            fts = lport.length + 2
        end
    else
        stf = " " * 8
        fts = 13
    end
    puts ""
    puts "Unicorn Options"
    puts "==============="
    puts ""
    puts "    Option        Value#{stf}Description"
    puts "    ------        -----#{stf}-----------"
    printf "    %-14s%-#{fts}s%s\n", "LHOST", lhost, "Local host."
    printf "    %-14s%-#{fts}s%s\n", "LPORT", lport, "Local port."
    puts ""
end
