def readin_strict(sock, amo):
    data = ''
    while len(data) != amo:
        tdata = sock.recv(1)
        if tdata == '':
                raise Exception, 'AFMOTEMOTE> ZERO'
        data += tdata
    print str(map(ord, data))
    return data