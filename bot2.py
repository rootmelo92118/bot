from Linephu.linepy import *
from Linephu.akad.ttypes import *
import time
import timeit


client = LINE()
client.log("Auth Token : " + str(client.authToken))
#client = LINE('email', 'password')

oepoll = OEPoll(client)

MySelf = client.getProfile()
JoinedGroups = client.getGroupIdsJoined()
print("My MID : " + MySelf.mid)

whiteListedMid = ["u52afe1d4ea5332242efacfeb9190d2a3", "u58bc30a989f932d0fd73ccb847107779", "u2a3fb897b9e40c92a5962c43ec178006", "u0fcc0258ddc63ea6feea223e1a571445", "ud417ada62140fb51e46c19ec43b5681b", "ueaff862c8ef0202b937bb2203794ef4a"]

#mymid : ""


def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if op.param1 not in JoinedGroups:
            if op.param2 in whiteListedMid:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
                client.inviteIntoGroup(op.param1, ["u2a3fb897b9e40c92a5962c43ec178006", "u0fcc0258ddc63ea6feea223e1a571445", "ud417ada62140fb51e46c19ec43b5681b", "ueaff862c8ef0202b937bb2203794ef4a"])
                client.sendMessage(op.param1, "該群權限所有者:")
                gm = client.getGroup(op.param1).creator.mid
                client.sendContact(op.param1, gm)
            else:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_INVITE_INTO_GROUP\n\n")
        return


def NOTIFIED_UPDATE_GROUP(op):
    group = client.getGroup(op.param1)
    if op.param2 not in whiteListedMid:
        if op.param2 not in group.creator.mid:
            if op.param3 == "4":
                if group.preventedJoinByTicket == False:
                    try:
                        client.reissueGroupTicket(op.param1)
                        group.preventedJoinByTicket = True
                        client.updateGroup(group)
                        client.kickoutFromGroup(op.param1, [op.param2])
                    except Exception as e:
                        print(e)


def NOTIFIED_KICKOUT_FROM_GROUP(op):
    group = client.getGroup(op.param1)
    try:
        if op.param3 == MySelf.mid:
            hb = open("hb.txt", "r")
            b = open("b.txt", "r")
            halfBlackListedMid = hb.readline()
            blackListedMid = b.readline()
            hb.close()
            b.close()
            if op.param2 not in halfBlackListedMid and op.param3 not in blackListedMid:
                hb = open("hb.txt", "w")
                hb.write(op.param2)
                hb.close()
                client.kickoutFromGroup(op.param1, [op.param2])
            elif op.param2 in halfBlackListedMid:
                b = open("b.txt", "w")
                b.write(op.param2)
                b.close()
                client.kickoutFromGroup(op.param1, [op.param2])
            JoinedGroups.remove(op.param1)
        else:
            if op.param3 in whiteListedMid:
                client.kickoutFromGroup(op.param1, [op.param2])
                group = client.getGroup(op.param1)
                if group.preventedJoinByTicket == True:
                    try:
                        group.preventedJoinByTicket = False
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
                else:
                    try:
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return


def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.toType == 0:
                    print("\n")
                    print("Private Chat Message Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Message : " + msg.text)
                    print("\n")
                    if msg._from in whiteListedMid:
                        if msg.text.startswith("/contact"):
                            str1 = find_between_r(msg.text, "/contact ", "")
                            client.sendContact(msg._from, str1)
                        if msg.text.startswith("/jgurlx"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                            group = client.getGroup(str1)
                            try:
                                client.reissueGroupTicket(str1)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                        elif msg.text.startswith("/jgurl"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                        if msg.text == "/mid":
                            client.sendMessage(msg._from, "名稱 : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\n權限等級 : 管理者")
                        if msg.text == "/speed":
                            time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            str1 = str(time0)
                            client.sendMessage(msg._from, str1)
                        if msg.text.startswith("/sm"):
                            str1 = find_between_r(msg.text, "mid: ", " mid")
                            str2 = find_between_r(msg.text, "text: ", " text")
                            client.sendMessage(str1, str2)
                        if msg.text.startswith("/sc"):
                            str1 = find_between_r(msg.text, "mid: ", " mid")
                            str2 = find_between_r(msg.text, "cmid: ", " cmid")
                            client.sendContact(str1, str2)
                        if msg.text.startswith("/kick"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "mid: ", " mid")
                            if str2 not in whiteListedMid:
                                try:
                                    client.kickoutFromGroup(str1, [str2])
                                except Exception as e:
                                    print(e)
                    elif msg._from in whiteListedMid:
                        if msg.text.startswith("/jgurlx"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                            group = client.getGroup(str1)
                            try:
                                client.reissueGroupTicket(str1)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                elif msg.toType == 1:
                    pass
                elif msg.toType == 2:
                    if msg._from in whiteListedMid:
                        print("\n")
                        print("Private Chat Message Received")
                        print("Sender's Name : " + client.getContact(msg._from).displayName)
                        print("Sender's MID : " + msg._from)
                        print("Received Message : " + msg.text)
                        print("\n")
                        if msg.text == "/gid":
                            client.sendMessage(msg.to, msg.to)
                        if msg.text == "/gcreator":
                            group = client.getGroup(msg.to)
                            ga = group.creator.mid
                            client.sendContact(msg.to, ga)
                        if msg.text == "/ginfo":
                            group = client.getGroup(msg.to)
                            md = "[群組名稱]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[群組圖片]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                            if group.preventedJoinByTicket is False:
                                md += "\n\n行動網址: 開啟\n"
                            else:
                                md += "\n\n行動網址: 關閉\n"
                            if group.invitee is None:
                                md += "\n成員數: " + str(len(group.members)) + "人\n\n邀請中: 0人"
                            else:
                                md += "\n成員數: " + str(len(group.members)) + "人\n邀請中: " + str(
                                    len(group.invitee)) + "人"
                                client.sendMessage(msg.to, md)
                                client.sendMessage(msg.to, "群長:")
                                gm = group.creator.mid
                                client.sendContact(msg.to, gm)
                        if msg.text == "/help":
                            client.sendMessage(msg.to, "群組指令:\n\n/gid\n/ginfo\n/kick <MID>\n/gurl on\n/gurl off\n/bye\nmk @")
                        if msg.text == "/speed":
                            time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            str1 = str(time0)
                            client.sendMessage(msg.to, str1)
                        if msg.text.startswith("/contact"):
                            str1 = find_between_r(msg.text, "/contact ", "")
                            client.sendContact(msg.to, str1)
                        if msg.text == "/mid":
                            client.sendMessage(msg.to, "名字 : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\n權限等級 : 5")
                        if msg.text == "/bye":
                            client.leaveGroup(msg.to)
                            JoinedGroups.remove(msg.to)
                        if msg.text == "/gurl on":
                            group = client.getGroup(msg.to)
                            try:
                                group.preventedJoinByTicket = False
                                str1 = client.reissueGroupTicket(msg.to)
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                            client.sendMessage(msg.to, "http://line.me/R/ti/g/" + str1)
                        if msg.text == "/gurl off":
                            group = client.getGroup(msg.to)
                            try:
                                client.reissueGroupTicket(msg.to)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                        if "mk " in msg.text:
                            key = eval(msg.contentMetadata["MENTION"])
                            key["MENTIONEES"][0]["M"]
                            targets = []
                            for x in key["MENTIONEES"]:
                                targets.append(x["M"])
                            for target in targets:
                                if target in whiteListedMid:
                                    pass
                                else:
                                    try:
                                        client.kickoutFromGroup(msg.to,[target])
                                    except:
                                        pass
                        if msg.text.startswith("/kick"):
                            str1 = find_between_r(msg.text, "/kick ", "")
                            if str1 not in whiteListedMid:
                                try:
                                    client.kickoutFromGroup(msg.to, [str1])
                                except Exception as e:
                                    print(e)
                                return
                else:
                    pass
            except:
                pass
        elif msg.contentType == 13:
            if msg.toType == 0:
                if msg._from in whiteListedMid:
                    x = op.message.contentMetadata
                    str1 = str(x)
                    str2 = find_between_r(str1, "'mid': '", "'")
                    str3 = find_between_r(str1, "'mid': '", "', '")
                    if "displayName" in str2:
                        strx = str(str3)
                        client.sendMessage(msg._from, strx)
                    else:
                        strx2 = str(str2)
                        client.sendMessage(msg._from, strx2)
                    print("\n")
                    print("Private Chat Contact Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Contact MID : " + str2)
                    print("Received Contact Display Name : " + client.getContact(str2).displayName)
                    print("\n")
                else:
                    x = op.message.contentMetadata
                    str1 = str(x)
                    str2 = find_between_r(str1, "'mid': '", "'")
                    str3 = find_between_r(str1, "'mid': '", "', '")
                    if "displayName" in str2 and str3 not in whiteListedMid:
                        strx = str(str3)
                        client.sendMessage(msg._from, strx)
                    elif str2 not in whiteListedMid:
                        strx2 = str(str2)
                        client.sendMessage(msg._from, strx2)
                    print("\n")
                    print("Private Chat Contact Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Contact MID : " + str2)
                    print("Received Contact Display Name : " + client.getContact(str2).displayName)
                    print("\n")
            elif msg.toType == 1:
                pass
            elif msg.toType == 2:
                x = op.message.contentMetadata
                str1 = str(x)
                str2 = find_between_r(str1, "'mid': '", "'")
                str3 = find_between_r(str1, "'mid': '", "', '")
                if "displayName" in str2 and str3 not in whiteListedMid:
                    strx = str(str3)
                    client.sendMessage(msg.to, strx)
                elif str2 not in whiteListedMid:
                    strx2 = str(str3)
                    client.sendMessage(msg.to, strx2)
                    print("Contact Received, MID : " + str2)
        else:
            pass
    except Exception as error:
        print(error)
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return


oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP,
    OpType.NOTIFIED_UPDATE_GROUP: NOTIFIED_UPDATE_GROUP,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


while True:
    oepoll.trace()
