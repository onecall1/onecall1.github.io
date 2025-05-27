from pptx import Presentation
from pptx.util import Inches
import os

def html_to_ppt():
    # HTML 파일 읽기
    html_file = "apm_price.html"
    
    print(f"HTML 파일 읽는 중: {html_file}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # PPT 생성
    prs = Presentation()
    
    # 슬라이드 크기를 1920x1080으로 설정 (16:9 비율)
    prs.slide_width = Inches(13.33)  # 1920px
    prs.slide_height = Inches(7.5)   # 1080px
    
    # 빈 슬라이드 레이아웃 사용
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    
    # HTML을 웹 객체로 삽입하는 방법
    # 임시 HTML 파일의 절대 경로 생성
    abs_html_path = os.path.abspath(html_file)
    file_url = f"file:///{abs_html_path.replace(os.sep, '/')}"
    
    print(f"HTML URL: {file_url}")
    
    # 웹 브라우저 객체 추가 (OLE 객체)
    try:
        # PowerPoint에서 웹 페이지를 삽입하는 방법
        # 이것은 실제로는 iframe과 같은 역할을 함
        
        # 대신 HTML을 이미지로 변환해서 삽입하는 방식 사용
        from playwright.sync_api import sync_playwright
        
        print("HTML을 고품질 이미지로 변환 중...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1920, 'height': 1080})
            
            # HTML 파일 로드
            page.goto(file_url, wait_until='networkidle')
            
            # 폰트와 스타일 완전 로딩 대기
            page.wait_for_timeout(3000)
            
            # 고품질 스크린샷 생성
            temp_image = "temp_slide.png"
            page.screenshot(path=temp_image, full_page=False)
            browser.close()
        
        # 이미지를 슬라이드에 삽입
        slide.shapes.add_picture(temp_image, Inches(0), Inches(0), 
                                width=prs.slide_width, height=prs.slide_height)
        
        # 임시 이미지 파일 삭제
        if os.path.exists(temp_image):
            os.remove(temp_image)
            
        print("HTML 스타일이 완벽하게 보존된 PPT 생성 완료")
        
    except Exception as e:
        print(f"웹 객체 삽입 실패: {e}")
        print("대체 방법으로 텍스트 기반 슬라이드 생성...")
        
        # 기존 텍스트 기반 방법으로 폴백
        from pptx.util import Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor
        
        # 제목 추가
        title_box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(11.33), Inches(1))
        title_frame = title_box.text_frame
        title_p = title_frame.paragraphs[0]
        title_p.text = "모니터링 솔루션 공급 견적서"
        title_p.alignment = PP_ALIGN.CENTER
        title_p.font.size = Pt(36)
        title_p.font.bold = True
    
    # PPT 저장
    ppt_filename = "apm_price_direct.pptx"
    prs.save(ppt_filename)
    print(f"PPT 저장됨: {ppt_filename}")
    
    return ppt_filename

if __name__ == "__main__":
    html_to_ppt() 