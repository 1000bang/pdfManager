from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import os
import re

class PDFEditor:
    """PDF 편집 도구 모음"""
    
    @staticmethod
    def natural_sort_key(filename):
        numbers = re.findall(r'\d+', filename)
        return [int(num) for num in numbers] if numbers else [0]
    
    @staticmethod
    def parse_page_numbers(input_str, max_page):
        """
        페이지 번호 문자열을 파싱
        예: "1,3,5" -> [1,3,5]
            "1-5" -> [1,2,3,4,5]
            "1,3-5,7" -> [1,3,4,5,7]
        """
        pages = set()
        parts = input_str.replace(' ', '').split(',')
        
        for part in parts:
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    pages.update(range(start, end + 1))
                except:
                    print(f"⚠️  잘못된 범위 형식: {part}")
            else:
                try:
                    pages.add(int(part))
                except:
                    print(f"⚠️  잘못된 숫자: {part}")
        
        valid_pages = sorted([p for p in pages if 1 <= p <= max_page])
        return valid_pages
    
    @staticmethod
    def merge_pdfs_interactive():
        # PDF 병합
        print("\n" + "="*60)
        print("📄 PDF 병합")
        print("="*60)
        
        # 폴더 경로 입력
        folder_path = input("\nPDF가 있는 폴더 경로 (엔터=현재 폴더): ").strip()
        if not folder_path:
            folder_path = '.'
        
        if not os.path.exists(folder_path):
            print(f"❌ 폴더를 찾을 수 없습니다: {folder_path}")
            return
        
        # PDF 파일 검색
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print("❌ PDF 파일이 없습니다.")
            return
        
        # 숫자 순서로 정렬
        pdf_files.sort(key=PDFEditor.natural_sort_key)
        
        print(f"\n📋 발견된 PDF 파일 ({len(pdf_files)}개):")
        for i, pdf in enumerate(pdf_files, 1):
            print(f"  {i:2d}. {pdf}")
        
        # 출력 파일명 입력
        print("\n💾 저장할 파일명을 입력하세요")
        output_name = input("   (예: merged.pdf): ").strip()
        
        if not output_name:
            output_name = 'merged_output.pdf'
        
        if not output_name.endswith('.pdf'):
            output_name += '.pdf'
        
        # 확인
        print(f"\n병합 순서: {len(pdf_files)}개 파일")
        print(f"저장 파일: {output_name}")
        confirm = input("\n병합을 시작하시겠습니까? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ 취소되었습니다.")
            return
        
        # 병합 실행
        try:
            merger = PdfMerger()
            print("\n🔄 병합 중...")
            
            for idx, pdf_file in enumerate(pdf_files, 1):
                file_path = os.path.join(folder_path, pdf_file)
                print(f"  [{idx}/{len(pdf_files)}] {pdf_file}")
                merger.append(file_path)
            
            print(f"\n💾 저장 중: {output_name}")
            merger.write(output_name)
            merger.close()
            
            file_size = os.path.getsize(output_name)
            print("\n" + "="*60)
            print("✅ 병합 완료!")
            print("="*60)
            print(f"📁 저장 위치: {os.path.abspath(output_name)}")
            print(f"📊 파일 크기: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
    
    @staticmethod
    def delete_pages_interactive():
        #페이지 삭제
        print("\n" + "="*60)
        print("🗑️  PDF 페이지 삭제")
        print("="*60)
        
        # 파일명 입력
        input_pdf = input("\n📄 원본 PDF 파일명: ").strip()
        
        if not os.path.exists(input_pdf):
            print(f"❌ 파일을 찾을 수 없습니다: {input_pdf}")
            return
        
        try:
            # PDF 정보 표시
            reader = PdfReader(input_pdf)
            total_pages = len(reader.pages)
            
            print(f"\n📊 총 페이지 수: {total_pages}")
            print(f"    (1 ~ {total_pages} 범위)")
            
            # 삭제할 페이지 입력
            print("\n🗑️  삭제할 페이지 번호를 입력하세요")
            print("    형식 예시:")
            print("    - 개별: 1,3,5")
            print("    - 범위: 1-5")
            print("    - 혼합: 1,3-5,7,10-12")
            print("    - 홀수: odd 또는 홀수")
            print("    - 짝수: even 또는 짝수")
            # --- 옵션추가 홀,짝수 페이지 삭제 ---
            print("    - **시작 페이지 포함 홀수**: 5 odd 또는 5 홀수 (5, 7, 9, ... 삭제)")
            print("    - **시작 페이지 포함 짝수**: 6 even 또는 6 짝수 (6, 8, 10, ... 삭제)")
            # -----------------------------------
            
            pages_input = input("\n삭제할 페이지: ").strip()
            
            pages_to_delete = []
            
            # 홀수/짝수 처리 (전체)
            if pages_input.lower() in ['odd', '홀수']:
                pages_to_delete = [i for i in range(1, total_pages + 1) if i % 2 == 1]
                print(f"\n홀수 페이지 선택됨: {pages_to_delete[:10]}{'...' if len(pages_to_delete) > 10 else ''}")
            elif pages_input.lower() in ['even', '짝수']:
                pages_to_delete = [i for i in range(1, total_pages + 1) if i % 2 == 0]
                print(f"\n짝수 페이지 선택됨: {pages_to_delete[:10]}{'...' if len(pages_to_delete) > 10 else ''}")
            else:
                # 시작 페이지 지정 + 홀수/짝수 처리
                parts = pages_input.split()
                if len(parts) == 2:
                    try:
                        start_page = int(parts[0])
                        option = parts[1].lower()
                        
                        if 1 <= start_page <= total_pages:
                            if option in ['odd', '홀수']:
                                # 시작 페이지부터 total_pages까지 중 홀수 페이지 선택
                                pages_to_delete = [i for i in range(start_page, total_pages + 1) if i % 2 == 1]
                                print(f"\n{start_page} 페이지부터 홀수 페이지 선택됨: {pages_to_delete[:10]}{'...' if len(pages_to_delete) > 10 else ''}")
                            elif option in ['even', '짝수']:
                                # 시작 페이지부터 total_pages까지 중 짝수 페이지 선택
                                pages_to_delete = [i for i in range(start_page, total_pages + 1) if i % 2 == 0]
                                print(f"\n{start_page} 페이지부터 짝수 페이지 선택됨: {pages_to_delete[:10]}{'...' if len(pages_to_delete) > 10 else ''}")
                            
                            # 새로운 옵션으로 처리된 경우, 기존 parse_page_numbers 호출 방지
                            if pages_to_delete:
                                pass 
                            else:
                                # 페이지 번호 파싱 (기존 로직)
                                pages_to_delete = PDFEditor.parse_page_numbers(pages_input, total_pages)
                        else:
                            print(f"⚠️ 시작 페이지 번호 ({start_page})가 유효한 범위 (1 ~ {total_pages})를 벗어납니다. 기존 방식으로 파싱합니다.")
                            # 페이지 번호 파싱 (기존 로직)
                            pages_to_delete = PDFEditor.parse_page_numbers(pages_input, total_pages)
                    except ValueError:
                        # '숫자 옵션' 패턴이 아니면 기존 로직으로 처리
                        # 페이지 번호 파싱 (기존 로직)
                        pages_to_delete = PDFEditor.parse_page_numbers(pages_input, total_pages)
                else:
                    # 페이지 번호 파싱 (기존 로직)
                    pages_to_delete = PDFEditor.parse_page_numbers(pages_input, total_pages)
            
            if not pages_to_delete:
                print("❌ 삭제할 페이지가 없습니다.")
                return
            
            # 페이지 번호는 정렬되고 중복이 없어야 함
            pages_to_delete = sorted(list(set(pages_to_delete)))
            
            pages_to_keep_count = total_pages - len(pages_to_delete)
            
            print(f"\n삭제할 페이지 ({len(pages_to_delete)}개): ", end="")
            if len(pages_to_delete) <= 20:
                print(pages_to_delete)
            else:
                print(f"{pages_to_delete[:10]} ... {pages_to_delete[-10:]}")
            print(f"유지할 페이지: {pages_to_keep_count}개")
            
            if pages_to_keep_count == 0:
                print("❌ 모든 페이지를 삭제할 수 없습니다.")
                return
            
            # 출력 파일명 입력
            default_output = f"{os.path.splitext(input_pdf)[0]}_edited.pdf"
            print(f"\n💾 저장할 파일명")
            output_pdf = input(f"    (엔터='{default_output}'): ").strip()
            
            if not output_pdf:
                output_pdf = default_output
            
            if not output_pdf.endswith('.pdf'):
                output_pdf += '.pdf'
            
            # 확인
            confirm = input("\n계속하시겠습니까? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ 취소되었습니다.")
                return
            
            # 페이지 삭제 실행
            writer = PdfWriter()
            # PDF 페이지 인덱스는 0부터 시작하므로, 입력된 페이지 번호(1부터 시작)를 조정합니다.
            pages_to_delete_set = set(p - 1 for p in pages_to_delete)
            
            print("\n🔄 처리 중...")
            for i in range(total_pages):
                if i not in pages_to_delete_set:
                    writer.add_page(reader.pages[i])
            
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            
            file_size = os.path.getsize(output_pdf)
            
            print("\n" + "="*60)
            print("✅ 페이지 삭제 완료!")
            print("="*60)
            print(f"📁 저장 위치: {os.path.abspath(output_pdf)}")
            # 파일 크기 포맷을 더 읽기 쉽게 수정
            print(f"📊 파일 크기: {file_size:,} bytes ({(file_size/1024):.1f} KB / {(file_size/1024/1024):.2f} MB)")
            print(f"📄 최종 페이지: {pages_to_keep_count}개")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")


    
    @staticmethod
    def extract_pages_interactive():
        #대화형 페이지 추출
        print("\n" + "="*60)
        print("📑 PDF 페이지 추출")
        print("="*60)
        
        # 파일명 입력
        input_pdf = input("\n📄 원본 PDF 파일명: ").strip()
        
        if not os.path.exists(input_pdf):
            print(f"❌ 파일을 찾을 수 없습니다: {input_pdf}")
            return
        
        try:
            # PDF 정보 표시
            reader = PdfReader(input_pdf)
            total_pages = len(reader.pages)
            
            print(f"\n📊 총 페이지 수: {total_pages}")
            print(f"   (1 ~ {total_pages} 범위)")
            
            # 추출할 페이지 입력
            print("\n📑 추출할 페이지 번호를 입력하세요")
            print("   형식 예시:")
            print("   - 개별: 1,3,5")
            print("   - 범위: 1-5")
            print("   - 혼합: 1,3-5,7,10-12")
            print("   - 전체: all")
            
            pages_input = input("\n추출할 페이지: ").strip()
            
            # 전체 페이지 처리
            if pages_input.lower() == 'all':
                pages_to_extract = list(range(1, total_pages + 1))
            else:
                pages_to_extract = PDFEditor.parse_page_numbers(pages_input, total_pages)
            
            if not pages_to_extract:
                print("❌ 추출할 페이지가 없습니다.")
                return
            
            print(f"\n추출할 페이지 ({len(pages_to_extract)}개): {pages_to_extract}")
            
            # 출력 파일명 입력
            default_output = f"{os.path.splitext(input_pdf)[0]}_extracted.pdf"
            print(f"\n💾 저장할 파일명")
            output_pdf = input(f"   (엔터='{default_output}'): ").strip()
            
            if not output_pdf:
                output_pdf = default_output
            
            if not output_pdf.endswith('.pdf'):
                output_pdf += '.pdf'
            
            # 확인
            confirm = input("\n계속하시겠습니까? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ 취소되었습니다.")
                return
            
            # 페이지 추출 실행
            writer = PdfWriter()
            
            print("\n🔄 처리 중...")
            for page_num in pages_to_extract:
                writer.add_page(reader.pages[page_num - 1])
            
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            
            file_size = os.path.getsize(output_pdf)
            
            print("\n" + "="*60)
            print("✅ 페이지 추출 완료!")
            print("="*60)
            print(f"📁 저장 위치: {os.path.abspath(output_pdf)}")
            print(f"📊 파일 크기: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            print(f"📄 추출된 페이지: {len(pages_to_extract)}개")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")


def main_menu():
    # 메인 메뉴
    while True:
        print("\n" + "="*60)
        print("📚 PDF 편집 도구")
        print("="*60)
        print("1. 📄 PDF 병합 (여러 PDF를 하나로)")
        print("2. 🗑️  페이지 삭제 (특정 페이지 제거)")
        print("3. 📑 페이지 추출 (특정 페이지만 추출)")
        print("4. 🚪 종료")
        print("="*60)
        
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == '1':
            PDFEditor.merge_pdfs_interactive()
        elif choice == '2':
            PDFEditor.delete_pages_interactive()
        elif choice == '3':
            PDFEditor.extract_pages_interactive()
        elif choice == '4':
            print("\n👋 프로그램을 종료합니다.")
            break
        else:
            print("\n❌ 잘못된 선택입니다. 1-4 중에서 선택하세요.")
        
        input("\n엔터를 눌러 메인 메뉴로 돌아갑니다...")


if __name__ == "__main__":
    print("="*60)
    print("PDF 편집 도구를 시작합니다")
    print("="*60)
    main_menu()