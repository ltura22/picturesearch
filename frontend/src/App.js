import React, { useState, useEffect } from "react";
import styled from "styled-components";
import {
  FiImage,
  FiSearch,
  FiRefreshCw,
  FiFolder,
  FiEye,
} from "react-icons/fi";
import axios from "axios";
import "./App.css";

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    sans-serif;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 40px;
  color: white;
`;

const Title = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 10px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.9;
  font-weight: 300;
`;

const MainContainer = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
    gap: 20px;
  }
`;

const Card = styled.div`
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: fit-content;
`;

const CardTitle = styled.h2`
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const TextArea = styled.textarea`
  width: 100%;
  min-height: 120px;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  padding: 15px;
  font-size: 16px;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  &::placeholder {
    color: #9ca3af;
  }
`;

const Button = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  margin-top: 15px;
  width: 100%;
  justify-content: center;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const ResultContainer = styled.div`
  margin-top: 20px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #667eea;
`;

const ResultLabel = styled.div`
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
`;

const ResultText = styled.div`
  color: #6b7280;
  line-height: 1.6;
`;

const StatsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-top: 15px;
`;

const StatCard = styled.div`
  background: white;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
`;

const StatValue = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
`;

const StatLabel = styled.div`
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 4px;
`;

const ExampleButton = styled.button`
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #4a5568;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  margin: 5px;
  transition: all 0.2s ease;

  &:hover {
    background: #e2e8f0;
    transform: none;
    box-shadow: none;
  }
`;

const ExampleContainer = styled.div`
  margin: 15px 0;
`;

const ExampleLabel = styled.div`
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
  font-weight: 500;
`;

const LoadingSpinner = styled.div`
  animation: spin 1s linear infinite;

  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
`;

const ProcessContainer = styled.div`
  margin-top: 20px;
  padding: 20px;
  background: #f0f9ff;
  border-radius: 12px;
  border-left: 4px solid #0ea5e9;
`;

const ProcessStep = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-bottom: 15px;
  color: #0f172a;
  font-size: 14px;

  &.active {
    color: #0ea5e9;
    font-weight: 600;
  }

  &.completed {
    color: #10b981;
  }
`;

const ProcessHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const ProcessOutput = styled.div`
  margin-left: 30px;
  padding: 8px 12px;
  background: #f8fafc;
  border-left: 3px solid #e2e8f0;
  border-radius: 0 6px 6px 0;
  font-size: 12px;
  color: #6b7280;
  font-style: italic;

  &.active {
    background: #eff6ff;
    border-left-color: #0ea5e9;
    color: #0369a1;
  }

  &.completed {
    background: #f0fdf4;
    border-left-color: #10b981;
    color: #065f46;
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
`;

const EmptyIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
`;

const EmptyText = styled.div`
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 5px;
`;

const EmptySubtext = styled.div`
  font-size: 14px;
  opacity: 0.7;
`;

const ProcessIcon = styled.div`
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;

  &.active {
    background: #0ea5e9;
    color: white;
  }

  &.completed {
    background: #10b981;
    color: white;
  }

  &.pending {
    background: #e2e8f0;
    color: #6b7280;
  }
`;

const PicturesContainer = styled.div`
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
`;

const PictureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 20px;
`;

const PictureCard = styled.div`
  background: #f8fafc;
  border-radius: 12px;
  padding: 15px;
  text-align: center;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;

  &:hover {
    border-color: #667eea;
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
  }
`;

const PictureImage = styled.img`
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
  background: #f3f4f6;
`;

const PictureName = styled.div`
  font-size: 11px;
  color: #374151;
  font-weight: 600;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const PictureType = styled.div`
  font-size: 9px;
  color: #667eea;
  background: #e0e7ff;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 5px;
`;

const PictureTags = styled.div`
  font-size: 8px;
  color: #6b7280;
  opacity: 0.8;
`;

const ProcessInput = styled.div`
  margin-left: 30px;
  padding: 6px 10px;
  background: #fef3c7;
  border-left: 3px solid #f59e0b;
  border-radius: 0 4px 4px 0;
  font-size: 11px;
  color: #92400e;
  font-weight: 500;
  margin-bottom: 4px;
`;

function App() {
  const [photoInput, setPhotoInput] = useState("");
  const [photoResult, setPhotoResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchProcess, setSearchProcess] = useState([]);
  const [pictures, setPictures] = useState([]);
  const [allPictures, setAllPictures] = useState([]);
  const [searchCompleted, setSearchCompleted] = useState(false);

  const photoExamples = [
    "ჩემს საქაღალდეში მიპოვე ფოტოები რომელშიც ჩანს ცხენზე მჯდომი კაცი",
    "მიპოვე ფოტო რომელშიც ჩანს წითელი მანქანა",
    "რა კარგი დღეა",
    "მინახე 4 ფოტო რომელშიც არის ძაღლი რომელიც ყეფს",
  ];

  // Fetch all available pictures on component mount
  useEffect(() => {
    const fetchAllPictures = async () => {
      try {
        const response = await axios.get("http://localhost:5001/pictures");
        if (response.data.pictures) {
          setAllPictures(response.data.pictures);
        }
      } catch (error) {
        console.error("Error fetching pictures:", error);
        setAllPictures([]);
      }
    };

    fetchAllPictures();
  }, []);

  const simulateSearchProcess = async (query) => {
    try {
      const response = await axios.post("http://localhost:5001/process-steps", {
        text: query,
      });

      if (response.data.success) {
        const realSteps = response.data.steps.map((step) => ({
          id: step.id,
          text: step.title,
          input: step.input,
          output: step.output,
          status: "pending",
        }));

        setSearchProcess(realSteps);

        // Animate through each step with real outputs
        realSteps.forEach((step, index) => {
          setTimeout(() => {
            setSearchProcess((prev) =>
              prev.map((s) =>
                s.id === step.id ? { ...s, status: "active" } : s
              )
            );

            setTimeout(() => {
              setSearchProcess((prev) =>
                prev.map((s) =>
                  s.id === step.id ? { ...s, status: "completed" } : s
                )
              );

              // On the last step, show the matched pictures only if it's a photo search
              if (step.id === 5) {
                setTimeout(() => {
                  if (response.data.final_result.is_photo_search) {
                    const photoCount = response.data.final_result.photo_count;
                    const matchedPictures = allPictures.slice(
                      0,
                      Math.min(photoCount, allPictures.length)
                    );
                    setPictures(matchedPictures);
                  } else {
                    setPictures([]); // No pictures for non-search queries
                  }
                  setSearchCompleted(true);
                }, 500);
              }
            }, 1200);
          }, index * 1800);
        });

        return response.data.final_result;
      }
    } catch (error) {
      console.error("Error getting process steps:", error);
      return null;
    }
  };

  const handlePhotoSearch = async () => {
    if (!photoInput.trim()) return;

    setLoading(true);
    setSearchCompleted(false);
    setPictures([]); // Clear previous results

    try {
      // Get the actual processing steps and result
      const result = await simulateSearchProcess(photoInput);

      if (result) {
        setPhotoResult(result);
      } else {
        // Fallback to regular agent call
        const response = await axios.post("http://localhost:5001/agent", {
          text: photoInput,
        });

        if (response.data.success) {
          setPhotoResult(response.data.result);
        }
      }

      setTimeout(() => {
        setLoading(false);
      }, 10000); // Wait for process animation to complete
    } catch (error) {
      console.error("Error:", error);
      setLoading(false);
    }
  };

  const resetSearch = () => {
    setPhotoInput("");
    setPhotoResult(null);
    setSearchProcess([]);
    setPictures([]);
    setSearchCompleted(false);
    setLoading(false);
  };

  return (
    <AppContainer>
      <Header>
        <Title>
          <FiImage />
          Photo Search Agent
        </Title>
        <Subtitle>AI-Powered Georgian Photo Search & Analysis</Subtitle>
      </Header>

      <MainContainer>
        {/* Photo Search Agent Card - Left Side */}
        <Card>
          <CardTitle>
            <FiSearch />
            Search in Pictures
          </CardTitle>

          <TextArea
            placeholder="Enter photo search query in Georgian..."
            value={photoInput}
            onChange={(e) => setPhotoInput(e.target.value)}
            disabled={loading}
          />

          <ExampleContainer>
            <ExampleLabel>Try these examples:</ExampleLabel>
            {photoExamples.map((example, index) => (
              <ExampleButton
                key={index}
                onClick={() => setPhotoInput(example)}
                disabled={loading}
              >
                Example {index + 1}
              </ExampleButton>
            ))}
          </ExampleContainer>

          <Button
            onClick={handlePhotoSearch}
            disabled={loading || !photoInput.trim()}
          >
            {loading ? (
              <LoadingSpinner>
                <FiRefreshCw />
              </LoadingSpinner>
            ) : (
              <FiSearch />
            )}
            {loading ? "Searching..." : "Search in Pictures"}
          </Button>

          {searchCompleted && (
            <Button
              onClick={resetSearch}
              style={{
                background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                marginTop: "10px",
              }}
            >
              <FiRefreshCw />
              New Search
            </Button>
          )}

          {searchProcess.length > 0 && (
            <ProcessContainer>
              <ResultLabel>Search Process:</ResultLabel>
              {searchProcess.map((step) => (
                <ProcessStep key={step.id} className={step.status}>
                  <ProcessHeader>
                    <ProcessIcon className={step.status}>
                      {step.status === "completed"
                        ? "✓"
                        : step.status === "active"
                          ? "⟳"
                          : step.id}
                    </ProcessIcon>
                    {step.text}
                  </ProcessHeader>
                  {step.input && (
                    <ProcessInput>Input: {step.input}</ProcessInput>
                  )}
                  {step.output && (
                    <ProcessOutput className={step.status}>
                      {step.output}
                    </ProcessOutput>
                  )}
                </ProcessStep>
              ))}
            </ProcessContainer>
          )}

          {photoResult && searchCompleted && (
            <ResultContainer>
              <ResultLabel>Search Results:</ResultLabel>
              <ResultText>{photoResult.original}</ResultText>

              <ResultLabel style={{ marginTop: "15px" }}>Analysis:</ResultLabel>
              <ResultText>
                Photo Search: {photoResult.is_photo_search ? "Yes" : "No"}
              </ResultText>

              {photoResult.is_photo_search && (
                <>
                  <ResultLabel style={{ marginTop: "15px" }}>
                    Search Terms:
                  </ResultLabel>
                  <ResultText>{photoResult.simplified_query}</ResultText>
                </>
              )}

              <StatsContainer>
                <StatCard>
                  <StatValue>
                    {photoResult.is_photo_search
                      ? photoResult.photo_count
                      : "N/A"}
                  </StatValue>
                  <StatLabel>Photos Requested</StatLabel>
                </StatCard>
                <StatCard>
                  <StatValue>
                    {photoResult.is_photo_search ? pictures.length : "N/A"}
                  </StatValue>
                  <StatLabel>Found</StatLabel>
                </StatCard>
                <StatCard>
                  <StatValue>
                    {photoResult.is_photo_search
                      ? photoResult.processing_type === "simplify_pipeline"
                        ? "Smart"
                        : "Basic"
                      : "None"}
                  </StatValue>
                  <StatLabel>Processing</StatLabel>
                </StatCard>
              </StatsContainer>
            </ResultContainer>
          )}
        </Card>

        {/* Pictures Display - Right Side */}
        <PicturesContainer>
          <CardTitle>
            <FiFolder />
            {searchCompleted
              ? photoResult && photoResult.is_photo_search
                ? `Found Pictures (${pictures.length})`
                : "No Search Query"
              : "Available Pictures"}
          </CardTitle>

          {!searchCompleted && pictures.length === 0 ? (
            <EmptyState>
              <EmptyIcon>
                <FiSearch />
              </EmptyIcon>
              <EmptyText>Ready to Search</EmptyText>
              <EmptySubtext>Enter a search query to find pictures</EmptySubtext>
            </EmptyState>
          ) : searchCompleted && photoResult && !photoResult.is_photo_search ? (
            <EmptyState>
              <EmptyIcon>
                <FiEye />
              </EmptyIcon>
              <EmptyText>Not a Search Query</EmptyText>
              <EmptySubtext>
                This appears to be a general statement, not a photo search
                request
              </EmptySubtext>
            </EmptyState>
          ) : (
            <PictureGrid>
              {pictures.map((picture, index) => (
                <PictureCard key={index}>
                  <PictureImage
                    src={`http://localhost:5001${picture.url}`}
                    alt={picture.name}
                    onError={(e) => {
                      e.target.style.display = "none";
                    }}
                  />
                  <PictureName>{picture.name}</PictureName>
                  <PictureType>{picture.type}</PictureType>
                  <PictureTags>{picture.tags?.join(", ")}</PictureTags>
                </PictureCard>
              ))}
            </PictureGrid>
          )}
        </PicturesContainer>
      </MainContainer>
    </AppContainer>
  );
}

export default App;
