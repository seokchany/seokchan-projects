# 이 파일은 모든 실시간 대응 기능(방화벽, EDR, 알림)을 한 번에 테스트하기 위한 스크립트입니다.

import time
import sys
import os

# --- 테스트 환경 설정 ---
# 이 스크립트가 다른 폴더(installers, actions)의 모듈을 찾을 수 있도록 경로를 설정합니다.
try:
    # `remediation.py`는 같은 폴더에 있으므로 바로 임포트합니다.
    from remediation import (
        handle_block_ip, handle_unblock_ip,
        handle_block_port, handle_unblock_port,
        handle_quarantine_host, handle_release_isolation
    )
except ImportError as e:
    print(f"\n[오류] 필수 모듈을 찾을 수 없습니다: {e}")
    print("이 스크립트는 반드시 'agent' 폴더 안에서 실행해야 합니다.")
    sys.exit(1)


def run_full_test():
    """
    모든 대응 조치와 알림 기능을 순서대로 테스트합니다.
    """
    print("🚀 전체 대응 기능 테스트를 시작합니다...")
    print("⚠️  이 테스트는 실제 방화벽 규칙과 네트워크 어댑터를 변경합니다.")
    print("="*50)

    # --- 테스트에 사용할 변수 ---
    test_ip = "8.8.8.8"  # 구글 DNS IP로 테스트
    test_port = 8888
    
    # --- 1. IP 차단/해제 테스트 ---
    print(f"\n[1/3] IP 차단/해제 테스트 (대상 IP: {test_ip})")
    print("-" * 40)
    
    print("1-1. IP 차단을 시도합니다...")
    print("   -> '보안 위협 대응 완료' 알림이 뜨는지 확인하세요.")
    handle_block_ip(test_ip)
    time.sleep(5) # 사용자가 알림을 확인할 시간을 줍니다.

    print("\n1-2. IP 차단 해제를 시도합니다...")
    print("   -> '보안 규칙 업데이트' 알림이 뜨는지 확인하세요.")
    handle_unblock_ip(test_ip)
    time.sleep(5)

    # --- 2. 포트 차단/해제 테스트 ---
    print(f"\n[2/3] 포트 차단/해제 테스트 (대상 포트: {test_port})")
    print("-" * 40)
    
    print("2-1. 포트 차단을 시도합니다...")
    print("   -> '포트 차단 완료' 알림이 뜨는지 확인하세요.")
    handle_block_port(test_port)
    time.sleep(5)

    print("\n2-2. 포트 차단 해제를 시도합니다...")
    print("   -> '포트 규칙 업데이트' 알림이 뜨는지 확인하세요.")
    handle_unblock_port(test_port)
    time.sleep(5)
    
    # --- 3. 호스트 격리/해제 테스트 ---
    print("\n[3/3] 호스트 격리/해제 테스트")
    print("⚠️  경고: 이 테스트는 모든 네트워크 연결을 잠시 비활성화했다가 다시 활성화합니다.")
    print("-" * 40)
    
    # 사용자가 인지하고 진행할 수 있도록 확인 과정을 추가합니다.
    input("준비되었으면 Enter 키를 눌러 호스트 격리 테스트를 계속하세요...")

    print("\n3-1. 호스트 격리를 시도합니다...")
    print("   -> '네트워크 격리 실행' 알림이 뜨는지 확인하세요.")
    handle_quarantine_host()
    print("   -> 10초 후 자동으로 격리를 해제합니다.")
    time.sleep(10)

    print("\n3-2. 호스트 격리 해제를 시도합니다...")
    print("   -> '네트워크 격리 해제' 알림이 뜨는지 확인하세요.")
    handle_release_isolation()
    time.sleep(5)


    print("\n" + "="*50)
    print("✅ 모든 테스트가 완료되었습니다.")


if __name__ == "__main__":
    # 스크립트가 관리자 권한으로 실행되었는지 확인합니다.
    try:
        import ctypes
        is_admin = (ctypes.windll.shell32.IsUserAnAdmin() != 0)
    except Exception:
        is_admin = False

    if not is_admin:
        print("\n[오류] 이 테스트 스크립트는 관리자 권한으로 실행해야 합니다.")
        print("PowerShell 또는 cmd를 '관리자 권한으로 실행'한 뒤 다시 시도해주세요.")
    else:
        # winotify 라이브러리가 설치되어 있는지 확인합니다.
        try:
            import winotify
        except ImportError:
            print("\n[오류] 'winotify' 라이브러리가 설치되지 않았습니다.")
            print("테스트를 진행하기 전에 터미널에 'pip install winotify'를 입력하여 설치해주세요.")
        else:
            run_full_test()
