# 이전 강화 화면 경로를 유지하기 위한 호환 진입점입니다.
# 실제 UI는 일반 강화와 특수 강화가 분리된 special_enhancement_screen.gd를 사용합니다.
# 이 파일을 직접 참조하는 구형 Scene도 동일한 최신 강화 화면을 실행합니다.
class_name EnhancementScreen
extends "res://scripts/ui/special_enhancement_screen.gd"
